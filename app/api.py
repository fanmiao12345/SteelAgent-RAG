from fastapi import APIRouter
from app.schemas import (
    ChatRequest, ChatResponse,
    SteelWeightRequest, CarbonEmissionRequest, EnergyCostRequest,
    FaultDiagnosisRequest, ProductionIndicatorRequest,
)
from agents.security_agent import check_security
from agents.planner_agent import classify_query
from agents.retriever_agent import retrieve_knowledge
from agents.tool_agent import detect_and_run_tool
from agents.answer_agent import generate_answer
from agents.reflection_agent import reflect_answer
from memory.conversation_memory import conversation_memory
from security.audit_logger import log_request
from security.access_control import ROLE_PERMISSIONS
from tools.steel_weight_calculator import calculate_steel_weight
from tools.carbon_emission_calculator import calculate_carbon_emission
from tools.energy_cost_calculator import calculate_energy_cost
from tools.fault_diagnosis_tool import diagnose_fault
from tools.production_indicator_tool import calculate_indicators
from rag.vector_store import vector_store
from rag.document_loader import load_documents
from rag.splitter import split_document

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "project": "SteelAgent-RAG"}


@router.get("/roles")
def get_roles():
    return ROLE_PERMISSIONS


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # 1. 安全检查
    security_result = check_security(req.query, req.role)
    if security_result["decision"] == "deny":
        log_request(req.session_id, req.user_id, req.role, req.query, "deny")
        return ChatResponse(
            answer="您的请求已被安全系统拦截。",
            query_type="unsafe_request",
            plan=["安全检查"],
            citations=[],
            used_tools=[],
            security=security_result,
            reflection={"passed": False, "issues": ["请求被安全系统拦截"]},
        )

    # 2. 分类
    query_type = classify_query(req.query)
    plan = ["安全检查", "问题分类"]
    if security_result["decision"] == "degrade":
        plan.append("降级为角色允许范围内回答")

    # 3. 检索知识库
    retrieval = retrieve_knowledge(req.query, role=req.role)
    plan.append("检索知识库")

    # 4. 尝试工具调用
    tool_result = None
    used_tools = []
    if query_type in ["calculation", "fault_diagnosis", "production_analysis"]:
        tool_result = detect_and_run_tool(req.query, req.role)
        if tool_result:
            used_tools.append("tool")
            plan.append("调用工具")

    # 5. 获取历史
    history = conversation_memory.get_history(req.session_id)

    # 6. 生成回答
    plan.append("生成回答")
    answer = generate_answer(
        query=req.query,
        context=retrieval["context"],
        tool_result=tool_result,
        history=history,
        citations=retrieval["citations"],
        retrieval_errors=retrieval.get("errors", []),
    )

    # 7. 反思检查
    reflection = reflect_answer(answer, retrieval["citations"], req.query)

    # 8. 保存对话
    conversation_memory.save_turn(
        req.session_id, req.user_id, req.role, req.query, answer
    )

    # 9. 审计日志
    log_request(
        req.session_id, req.user_id, req.role, req.query,
        security_result["decision"],
        used_tools=used_tools,
        used_docs=[c["doc_id"] for c in retrieval["citations"]],
    )

    return ChatResponse(
        answer=answer,
        query_type=query_type,
        plan=plan,
        citations=retrieval["citations"],
        used_tools=used_tools,
        security=security_result,
        reflection=reflection,
    )


@router.post("/ingest")
def ingest_docs():
    docs = load_documents("data/docs")
    all_chunks = []
    for doc in docs:
        all_chunks.extend(split_document(doc))
    vector_store.build_index(all_chunks)
    return {
        "status": "success",
        "message": "documents ingested successfully",
        "doc_count": len(docs),
    }


@router.post("/tool/steel-weight")
def tool_steel_weight(req: SteelWeightRequest):
    return calculate_steel_weight(
        shape=req.shape,
        thickness_mm=req.thickness_mm,
        width_m=req.width_m,
        length_m=req.length_m,
        diameter_mm=req.diameter_mm,
        outer_diameter_mm=req.outer_diameter_mm,
        inner_diameter_mm=req.inner_diameter_mm,
    )


@router.post("/tool/carbon-emission")
def tool_carbon_emission(req: CarbonEmissionRequest):
    return calculate_carbon_emission(req.production_ton, req.emission_factor)


@router.post("/tool/energy-cost")
def tool_energy_cost(req: EnergyCostRequest):
    return calculate_energy_cost(
        req.electricity_kwh, req.electricity_price,
        req.gas_m3, req.gas_price,
    )


@router.post("/tool/fault-diagnosis")
def tool_fault_diagnosis(req: FaultDiagnosisRequest):
    return diagnose_fault(req.equipment, req.symptom)


@router.post("/tool/production-indicator")
def tool_production_indicator(req: ProductionIndicatorRequest):
    return calculate_indicators(req.csv_path)
