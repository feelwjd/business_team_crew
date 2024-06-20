import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import DirectoryReadTool
from decouple import config

os.environ["OPENAI_API_KEY"] = config('OPEN_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = config('OPENAI_MODEL_NAME')


tool = DirectoryReadTool()

# Creating a senior researcher agent with memory and verbose mode

baseDir = config('BASE_DIR')

business_idea_agent = Agent(
    role='Business Idea Agent',
    goal='사업 아이디어를 구체화하고 시장 조사를 수행합니다.',
    backstory="""당신은 창의적인 사고를 통해 새로운 사업 아이디어를 발굴하고 이를 구체화하는 역할을 맡고 있습니다. 시장 조사를 통해 아이디어의 타당성을 평가하고, 잠재적인 기회를 파악합니다.""",
    verbose=True,
    tools=[],  # 필요시 추가
    step_callback=None,
    cache=True,
)

business_idea_task = Task(
    description="사용자가 제시한 주제에 대해 사업 아이디어를 구체화하고 시장 조사를 수행합니다.",
    agent=business_idea_agent,
    expected_output="""
    사용자가 제시한 주제는 {subject}입니다. 사용자는 {description}라는 요구사항을 가지고 있습니다. 이에 따라, 다음과 같은 업무를 수행해야 합니다:

    1. 사업 아이디어 구체화:
       - subject에 대한 다양한 사업 아이디어를 제시하고, 각각의 장단점을 분석합니다.
       - 사용자의 요구사항 description을 반영하여, 가장 적합한 사업 아이디어를 선정합니다.

    2. 시장 조사:
       - subject와 관련된 시장 동향을 조사합니다.
       - 현재 시장에서 경쟁하고 있는 주요 업체와 그들의 비즈니스 모델을 분석합니다.
       - 타겟 시장의 수요와 트렌드를 파악하여, 사업 아이템의 시장 진입 가능성을 평가합니다.

    3. 사업 모델 제안:
       - 선정된 사업 아이디어를 기반으로 구체적인 비즈니스 모델을 제안합니다.
       - 수익 모델, 주요 고객층, 제공할 제품 및 서비스, 차별화 전략 등을 포함합니다.

    4. 초기 전략 수립:
       - 사업 아이템의 초기 전략을 수립합니다.
       - 제품 개발, 마케팅, 자금 조달, 파트너십 등 중요한 초기 단계의 계획을 제안합니다.

    이와 같은 내용을 바탕으로, subject에 대한 사업 아이디어를 구체화하고 시장 조사를 수행하여 사용자가 원하는 사업을 성공적으로 추진할 수 있도록 지원합니다.
    포맷은 markdown으로 해주고, 한글로 작성해야 합니다. 
    """,
    output_file=baseDir+'/1.md'
)

# def business_idea_callback(output):
#     global business_idea_result
#     result = output.raw_output.strip().split('\n')
#     business_idea_result = {
#         '사업 아이디어': result[0].split(': ')[1],
#         '장점과 단점': result[1].split(': ')[1],
#         '초기 전략': result[2].split(': ')[1]
#     }
# 
# business_idea_task = Task(
#     description="사용자가 제시한 주제 {subject}에 대해 사업 아이디어를 구체화하고, {description}의 요구사항을 반영해야합니다. 그리고 시장 조사를 수행합니다.",
#     agent=business_idea_agent,
#     expected_output="""
#     --으로 감싼 부분에 내용을 작성해야 합니다.
#     ex) --사업 아이디어--
#     그리고 markdown 포맷으로 작성해야 합니다.
#     
#     사업 아이디어: --사업 아이디어--
#     장점과 단점: --장점과 단점--
#     초기 전략: --초기 전략--
#     """,
#     #callback=business_idea_callback,
#     output_file=baseDir+'/1.md'
# )


market_research_agent = Agent(
    role='Market Research Agent',
    goal='시장 분석을 통해 비즈니스 모델을 수립합니다.',
    backstory="""당신은 시장 분석 전문가로서, 비즈니스 아이디어의 타당성을 검토하고 시장 동향, 경쟁사 분석, 소비자 분석을 통해 성공적인 비즈니스 모델을 수립하는 역할을 맡고 있습니다.""",
    verbose=True,
    tools=[],  # 필요시 추가
    step_callback=None,
    cache=True,
)

market_research_task = Task(
    description="Business Idea Agent의 결과를 바탕으로 시장 조사를 수행합니다.",
    agent=market_research_agent,
    expected_output="""
    Business Idea Agent가 제공한 사업 아이디어를 바탕으로 다음과 같은 시장 조사를 수행해야 합니다:

    1. 시장 분석:
       - 사업 아이디어와 관련된 글로벌 및 로컬 시장 동향을 분석합니다.
       - 해당 분야의 시장 규모, 성장률, 주요 트렌드를 조사합니다.
       - 시장의 주요 세그먼트를 식별하고, 각 세그먼트의 특징과 요구사항을 파악합니다.

    2. 경쟁 분석:
       - 사업 아이디어와 관련된 주요 경쟁 업체를 식별하고, 그들의 비즈니스 모델, 제품/서비스, 마케팅 전략을 분석합니다.
       - 각 경쟁 업체의 강점과 약점을 파악하고, 시장에서의 위치를 평가합니다.
       - 경쟁 업체와의 차별화 포인트를 도출합니다.

    3. 소비자 분석:
       - 타겟 시장의 주요 소비자 그룹을 정의하고, 이들의 요구사항, 선호도, 구매 패턴을 조사합니다.
       - 소비자 설문 조사, 인터뷰, 포커스 그룹 등을 통해 심층적인 소비자 인사이트를 수집합니다.
       - 소비자 행동 분석을 통해, 타겟 시장의 니즈와 페인 포인트를 파악합니다.

    4. SWOT 분석:
       - 사업 아이디어 사업 아이디어의 강점(Strengths), 약점(Weaknesses), 기회(Opportunities), 위협(Threats)을 분석합니다.
       - SWOT 분석을 통해, 사업 아이템의 성공 가능성을 평가하고, 전략적 방향을 제안합니다.

    5. 시장 진입 전략:
       - 조사된 시장 정보를 바탕으로, 최적의 시장 진입 전략을 제안합니다.
       - 제품/서비스의 포지셔닝, 가격 전략, 유통 채널, 마케팅 전략 등을 포함합니다.
       - 초기 시장 진입 시 직면할 수 있는 주요 리스크와 대응 방안을 제시합니다.

    이와 같은 내용을 바탕으로, 사업 아이디어에 대한 심층적인 시장 조사를 수행하여 사용자가 원하는 사업을 성공적으로 추진할 수 있도록 지원합니다.
    포맷은 markdown으로 해주고, 한글로 작성해야 합니다.
    """,
    output_file=baseDir+'/2.md'
)

# def market_research_callback(output):
#     global market_research_result
#     result = output.raw_output.strip().split('\n')
#     market_research_result = {
#         '시장 분석 결과': result[0].split(': ')[1],
#         '경쟁 분석 결과': result[1].split(': ')[1],
#         '소비자 분석 결과': result[2].split(': ')[1],
#         'SWOT 분석 결과': result[3].split(': ')[1],
#         '시장 진입 전략': result[4].split(': ')[1]
#     }
# 
# market_research_task = Task(
#     description="Business Idea Agent의 결과를 바탕으로 시장 조사를 수행합니다.",
#     agent=market_research_agent,
#     expected_output="""
#     --으로 감싼 부분에 내용을 작성해야 합니다.
#     ex) --사업 아이디어--
#     그리고 markdown 포맷으로 작성해야 합니다.
#     
#     시장 분석 결과: --시장 분석 결과--
#     경쟁 분석 결과: --경쟁 분석 결과--
#     소비자 분석 결과: --소비자 분석 결과--
#     SWOT 분석 결과: --SWOT 분석 결과--
#     시장 진입 전략: --시장 진입 전략--
#     """,
#     #callback=market_research_callback,
#     context=[business_idea_task],
#     output_file=baseDir+'/2.md'
# )


business_plan_agent = Agent(
    role='Business Plan Agent',
    goal='사업 계획서를 작성합니다.',
    backstory="""당신은 사업 계획 전문가로서, 시장 조사 결과를 바탕으로 구체적인 사업 계획서를 작성하고, 비즈니스 모델, 마케팅 전략, 재무 계획 등을 포함한 종합적인 계획을 수립하는 역할을 맡고 있습니다.""",
    verbose=True,
    tools=[],  # 필요시 추가
    step_callback=None,
    cache=True,
)

business_plan_task = Task(
    description="Market Research Agent의 결과를 바탕으로 사업 계획서를 작성합니다.",
    agent=business_plan_agent,
    expected_output="""
    Market Research Agent가 제공한 조사 결과를 바탕으로, 다음과 같은 업무를 수행하여 구체적인 사업 계획서를 작성해야 합니다:

    1. 사업 개요 작성:
       - 사업 아이디어와 이를 통해 해결하고자 하는 문제를 명확히 서술합니다.
       - 사업의 목표와 비전을 정의합니다.

    2. 시장 분석 요약:
       - 시장 분석 결과를 요약하여 사업 계획서에 포함합니다.
       - 시장 규모, 성장률, 주요 트렌드 등을 강조합니다.

    3. 경쟁 분석 요약:
       - 경쟁 분석 결과를 요약하여 주요 경쟁 업체와 그들의 강점 및 약점을 서술합니다.
       - 경쟁 업체와의 차별화 전략을 명확히 합니다.

    4. 소비자 분석 요약:
       - 소비자 분석 결과를 요약하여 타겟 소비자 그룹의 요구사항과 선호도를 서술합니다.
       - 소비자 행동 패턴과 페인 포인트를 강조합니다.

    5. SWOT 분석 요약:
       - SWOT 분석 결과를 요약하여 사업의 강점, 약점, 기회, 위협을 명확히 합니다.
       - SWOT 분석을 바탕으로 전략적 방향을 제시합니다.

    6. 비즈니스 모델 수립:
       - 수익 모델, 주요 고객층, 제공할 제품 및 서비스, 차별화 전략 등을 구체적으로 제시합니다.
       - 비즈니스 모델 캔버스 또는 다른 시각적 도구를 사용하여 명확히 설명합니다.

    7. 마케팅 및 세일즈 전략:
       - 시장 진입 전략을 바탕으로 마케팅 및 세일즈 전략을 수립합니다.
       - 제품/서비스의 포지셔닝, 가격 전략, 유통 채널, 프로모션 전략 등을 구체적으로 서술합니다.

    8. 운영 계획:
       - 사업 운영에 필요한 주요 활동, 자원, 파트너십 등을 정의합니다.
       - 운영 계획에 필요한 인력, 기술, 설비 등을 서술합니다.

    9. 재무 계획:
       - 초기 자본 요구 사항, 수익 예측, 비용 구조 등을 포함한 재무 계획을 수립합니다.
       - 재무 예측을 통해 손익 분기점, 투자 회수 기간 등을 제시합니다.

    10. 리스크 관리 계획:
        - 사업 추진 시 예상되는 주요 리스크와 그에 대한 대응 방안을 제시합니다.

    이와 같은 내용을 바탕으로, 구체적이고 실행 가능한 사업 계획서를 작성하여 사용자가 원하는 사업을 성공적으로 추진할 수 있도록 지원합니다.
    포맷은 markdown으로 해주고, 한글로 작성해야 합니다.
    """,
    output_file=baseDir+'/3.md'
)

# def business_plan_callback(output):
#     global business_plan_result
#     result = output.raw_output.strip().split('\n')
#     business_plan_result = {
#         '사업 개요': result[0].split(': ')[1],
#         '시장 분석 요약': result[1].split(': ')[1],
#         '경쟁 분석 요약': result[2].split(': ')[1],
#         '소비자 분석 요약': result[3].split(': ')[1],
#         'SWOT 분석 요약': result[4].split(': ')[1],
#         '비즈니스 모델': result[5].split(': ')[1],
#         '마케팅 및 세일즈 전략': result[6].split(': ')[1],
#         '운영 계획': result[7].split(': ')[1],
#         '재무 계획': result[8].split(': ')[1],
#         '리스크 관리 계획': result[9].split(': ')[1]
#     }
# 
# business_plan_task = Task(
#     description="Market Research Agent의 결과를 바탕으로 사업 계획서를 작성합니다.",
#     agent=business_plan_agent,
#     expected_output="""
#     --으로 감싼 부분에 내용을 작성해야 합니다.
#     ex) --사업 아이디어--
#     그리고 markdown 포맷으로 작성해야 합니다.
#     
#     사업 개요: --사업 개요--
#     시장 분석 요약: --시장 분석 요약--
#     경쟁 분석 요약: --경쟁 분석 요약--
#     소비자 분석 요약: --소비자 분석 요약--
#     SWOT 분석 요약: --SWOT 분석 요약--
#     비즈니스 모델: --비즈니스 모델--
#     마케팅 및 세일즈 전략: --마케팅 및 세일즈 전략--
#     운영 계획: --운영 계획--
#     재무 계획: --재무 계획--
#     리스크 관리 계획: --리스크 관리 계획--
#     """,
#     #callback=business_plan_callback,
#     context=[market_research_task],
#     output_file=baseDir+'/3.md'
# )


requirement_definition_agent = Agent(
    role='Requirement Definition Agent',
    goal='사업 계획서를 바탕으로 기술적 요구사항을 정의합니다.',
    backstory="""당신은 시스템 요구사항 분석 전문가로서, 사업 계획서를 바탕으로 시스템 개발에 필요한 기능적 및 비기능적 요구사항을 정의하고, 이를 통해 프로젝트의 기술적 방향을 설정하는 역할을 맡고 있습니다.""",
    verbose=True,
    tools=[],  # 필요시 추가
    step_callback=None,
    cache=True,
)

requirement_definition_task = Task(
    description="Business Plan Agent의 결과를 바탕으로 기술적 요구사항을 정의합니다.",
    agent=requirement_definition_agent,
    expected_output="""
    Business Plan Agent가 제공한 사업 계획서의 결과를 바탕으로, 다음과 같은 업무를 수행하여 기술적 요구사항을 정의해야 합니다:

    1. 시스템 개요 정의:
       - 사업 개요를 바탕으로 시스템의 목적과 주요 기능을 명확히 서술합니다.
       - 시스템이 해결하고자 하는 문제와 기대 효과를 설명합니다.

    2. 기능적 요구사항 정의:
       - 시스템이 제공해야 하는 주요 기능들을 정의합니다.
       - 각 기능에 대한 상세 설명과 이를 통해 사용자에게 제공할 가치, 기능 간의 상호작용을 명확히 합니다.
       - 예를 들어, 사용자 관리, 제품 검색, 주문 처리, 결제 시스템 등의 주요 기능을 포함합니다.

    3. 비기능적 요구사항 정의:
       - 시스템의 성능, 보안, 확장성, 사용성, 유지보수성 등의 비기능적 요구사항을 정의합니다.
       - 각 비기능적 요구사항에 대해 측정 가능한 기준과 목표를 설정합니다.
       - 예를 들어, 응답 시간, 가용성, 데이터 보호 수준 등을 포함합니다.

    4. 시스템 아키텍처 요구사항:
       - 시스템 아키텍처의 주요 구성 요소와 이들의 상호작용을 정의합니다.
       - 데이터베이스 구조, 서버 구성, 네트워크 요구사항 등을 포함합니다.
       - 기술 스택(프로그래밍 언어, 프레임워크, 라이브러리 등)을 명확히 합니다.

    5. 데이터 요구사항 정의:
       - 시스템이 처리해야 하는 주요 데이터 유형과 이를 저장, 관리, 보호하는 방법을 정의합니다.
       - 데이터베이스 모델, 데이터 흐름, 데이터 무결성 및 보안 요구사항 등을 포함합니다.

    6. 인터페이스 요구사항 정의:
       - 시스템이 다른 시스템 또는 외부 서비스와 상호작용하는 방법을 정의합니다.
       - API, 사용자 인터페이스, 외부 시스템과의 통합 방법 등을 포함합니다.

    7. 사용자 요구사항 정의:
       - 타겟 사용자 그룹의 요구사항과 기대를 정의합니다.
       - 사용자 경험(UX)과 사용자 인터페이스(UI) 요구사항을 명확히 합니다.
       - 접근성, 다국어 지원, 사용자 피드백 메커니즘 등을 포함합니다.

    8. 프로젝트 관리 요구사항 정의:
       - 시스템 개발 및 배포를 위한 일정, 인력, 예산 등의 요구사항을 정의합니다.
       - 프로젝트 관리 도구와 방법론을 명확히 합니다.

    이와 같은 내용을 바탕으로, 사업 개요에 대한 기술적 요구사항을 체계적으로 정의하여 시스템 개발이 원활하게 이루어질 수 있도록 지원합니다.
    포맷은 markdown으로 해주고, 한글로 작성해야 합니다.
    """,
    output_file=baseDir+'/4.md'
)

# def requirement_definition_callback(output):
#     global requirement_definition_result
#     result = output.raw_output.strip().split('\n')
#     requirement_definition_result = {
#         '시스템 개요': result[0].split(': ')[1],
#         '기능적 요구사항': result[1].split(': ')[1],
#         '비기능적 요구사항': result[2].split(': ')[1],
#         '시스템 아키텍처 요구사항': result[3].split(': ')[1],
#         '데이터 요구사항': result[4].split(': ')[1],
#         '인터페이스 요구사항': result[5].split(': ')[1],
#         '사용자 요구사항': result[6].split(': ')[1],
#         '프로젝트 관리 요구사항': result[7].split(': ')[1]
#     }
# 
# requirement_definition_task = Task(
#     description="Business Plan Agent의 결과를 바탕으로 기술적 요구사항을 정의합니다.",
#     agent=requirement_definition_agent,
#     expected_output="""
#     --으로 감싼 부분에 내용을 작성해야 합니다.
#     ex) --사업 아이디어--
#     그리고 markdown 포맷으로 작성해야 합니다.
#     
#     시스템 개요: --시스템 개요--
#     기능적 요구사항: --기능적 요구사항--
#     비기능적 요구사항: --비기능적 요구사항--
#     시스템 아키텍처 요구사항: --시스템 아키텍처 요구사항--
#     데이터 요구사항: --데이터 요구사항--
#     인터페이스 요구사항: --인터페이스 요구사항--
#     사용자 요구사항: --사용자 요구사항--
#     프로젝트 관리 요구사항: --프로젝트 관리 요구사항--
#     """,
#     #callback=requirement_definition_callback,
#     context=[business_plan_task],
#     output_file=baseDir+'/4.md'
# )


# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
    agents=[business_idea_agent, market_research_agent, business_plan_agent, requirement_definition_agent],
    tasks=[business_idea_task, market_research_task, business_plan_task, requirement_definition_task],
    process=Process.sequential,  # Optional: Sequential task execution is default
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

inputs = {'subject': '대학생들에게 실무 경험을 제공하고, 기업에게는 저렴하고 유연한 인재 활용 기회를 제공하는 소규모 프로젝트 단위 고용 및 관리 플랫폼 구축',
          'description': '대학생들에게 실무 경험을 제공하고, 기업에게는 저렴하고 유연한 인재 활용 기회를 제공하는 소규모 프로젝트 단위 고용 및 관리 플랫폼 구축하여 스타트업을 창업. 추후에 글로벌한 회사로 성장시키고 싶음.'}
# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs=inputs)
print(result)
