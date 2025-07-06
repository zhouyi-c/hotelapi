import json
from langchain.chat_models import ChatOpenAI
from agents.manager_agent import ManagerAgent
from config import Config
from datetime import datetime


# 加载测试用例
def load_test_cases(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)



judge_llm = ChatOpenAI(
            api_key=Config.QIANFAN_API_KEY,
            base_url=Config.QIANFAN_BASE_URL,
            model=Config.QIANFAN_MODEL,
            temperature=0.7
        )
# evaluate.py
import re
import json


def safe_json_parse(text):
    """尝试从文本中提取有效的JSON"""
    try:
        # 尝试直接解析
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            # 尝试提取JSON部分
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except:
            return None
    return None


def evaluate_response(user_input, ideal_output, agent_response):
    # 增强约束的提示词
    prompt = f"""
    ## 客服回复质量评估任务
    **用户问题**: {user_input}
    **理想回复**: {ideal_output}
    **待评估回复**: {agent_response}

    ### 评估维度
    1. 专业性（是否符合酒店服务标准）: 0-10分
    2. 问题解决度（是否解决核心诉求）: 0-10分
    3. 情感适宜度（语气是否恰当）: 0-10分
    4. 格式规范性（是否符合业务要求）: 0-10分

    ### 评级标准
    - 优秀：三项以上维度达到8分以上
    - 合格：基本满足要求但有改进空间
    - 不合格：有重大缺陷或拒绝处理

    ### 输出要求
    - 只返回JSON格式数据，不要包含任何其他文本
    - JSON结构必须严格遵循以下格式：
    {{
        "rating": "优秀|合格|不合格",
        "reason": "评估理由（50字内）",
        "dimension_scores": {{
            "professionalism": 分数,
            "problem_solving": 分数,
            "tone": 分数,
            "compliance": 分数
        }}
    }}

    ### 重要提示
    请确保：
    1. 只返回JSON对象，不要包含任何其他内容
    2. JSON格式正确无误
    3. 评分是整数（0-10）
    """

    try:
        evaluation = judge_llm.predict(prompt)
        print(f"📝 评估原始响应: {evaluation}")  # 添加调试日志

        # 使用安全解析方法
        parsed = safe_json_parse(evaluation)
        if parsed:
            return parsed
        else:
            print("❌ 无法解析评估响应")
            raise ValueError("无法解析JSON")
    except Exception as e:
        print(f"❌ 评估解析失败: {str(e)}")
        return {
            "rating": "不合格",
            "reason": "评估解析失败",
            "dimension_scores": {
                "professionalism": 0,
                "problem_solving": 0,
                "tone": 0,
                "compliance": 0
            }
        }


# 主评估流程
def main():
    # 加载测试用例
    test_cases = load_test_cases("hotel-management/evaluation/test_cases.json")

    # 初始化Agent
    agent = ManagerAgent()

    results = []

    print(f"🚀 开始评估 {len(test_cases)} 个测试用例...")

    for case in test_cases:
        print(f"\n🔍 处理用例 [{case['id']}]: {case['input']}")

        # 获取Agent回复
        response = agent.route_task(case["input"])
        print(f"💬 Agent回复: {response}")

        # 评估回复质量
        evaluation = evaluate_response(
            case["input"],
            case["ideal_output"],
            response
        )

        # 保存结果
        result = {
            "test_id": case["id"],
            "category": case["category"],
            "difficulty": case["difficulty"],
            "user_input": case["input"],
            "ideal_output": case["ideal_output"],
            "agent_response": response,
            "evaluation": evaluation
        }

        results.append(result)
        print(f"✅ 评估结果: {evaluation['rating']} - {evaluation['reason']}")

    # 生成报告
    generate_report(results)

    print("\n🎉 评估完成！查看报告: evaluation_report.html")


# 生成可视化报告
def generate_report(results):
    import os
    os.makedirs("evaluation",exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"evaluation/report_{timestamp}.json"
    html_path = f"evaluation/report_{timestamp}.html"

    # 保存JSON报告
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 生成HTML报告
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>客服Agent评估报告</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .case { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; }
            .excellent { background-color: #e6ffe6; }
            .qualified { background-color: #ffffe6; }
            .unqualified { background-color: #ffe6e6; }
            .rating { font-weight: bold; margin-bottom: 10px; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>客服Agent评估报告</h1>
        <p>生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>

        <h2>概览统计</h2>
        <div id="summary"></div>

        <h2>详细结果</h2>
        <div id="details"></div>

        <script>
            const reportData = """ + json.dumps(results) + """;

            // 渲染概览统计
            function renderSummary() {
                const ratings = { '优秀': 0, '合格': 0, '不合格': 0 };
                const categories = {};

                reportData.forEach(item => {
                    ratings[item.evaluation.rating] = (ratings[item.evaluation.rating] || 0) + 1;

                    if (!categories[item.category]) {
                        categories[item.category] = { total: 0, ratings: { '优秀': 0, '合格': 0, '不合格': 0 } };
                    }

                    categories[item.category].total += 1;
                    categories[item.category].ratings[item.evaluation.rating] += 1;
                });

                let html = `<p>总用例数: ${reportData.length}</p>`;
                html += '<h3>评级分布</h3><ul>';

                for (const [rating, count] of Object.entries(ratings)) {
                    html += `<li>${rating}: ${count} (${(count/reportData.length*100).toFixed(1)}%)</li>`;
                }

                html += '</ul><h3>按场景统计</h3><table><tr><th>场景</th><th>用例数</th><th>优秀</th><th>合格</th><th>不合格</th></tr>';

                for (const [category, data] of Object.entries(categories)) {
                    html += `<tr>
                        <td>${category}</td>
                        <td>${data.total}</td>
                        <td>${data.ratings['优秀']}</td>
                        <td>${data.ratings['合格']}</td>
                        <td>${data.ratings['不合格']}</td>
                    </tr>`;
                }

                html += '</table>';
                document.getElementById('summary').innerHTML = html;
            }

            // 渲染详细结果
            function renderDetails() {
                let html = '';

                reportData.forEach(item => {
                    const ratingClass = item.evaluation.rating.toLowerCase();

                    html += `<div class="case ${ratingClass}">
                        <div class="rating">${item.test_id} | ${item.category} | 难度: ${item.difficulty} | 评级: <span class="${ratingClass}">${item.evaluation.rating}</span></div>
                        <p><strong>用户输入:</strong> ${item.user_input}</p>
                        <p><strong>Agent回复:</strong> ${item.agent_response}</p>
                        <p><strong>理想回复:</strong> ${item.ideal_output}</p>
                        <p><strong>评估理由:</strong> ${item.evaluation.reason}</p>

                        <table>
                            <tr><th>维度</th><th>评分</th></tr>
                            <tr><td>专业性</td><td>${item.evaluation.dimension_scores.professionalism}/10</td></tr>
                            <tr><td>问题解决</td><td>${item.evaluation.dimension_scores.problem_solving}/10</td></tr>
                            <tr><td>情感表达</td><td>${item.evaluation.dimension_scores.tone}/10</td></tr>
                            <tr><td>规范符合</td><td>${item.evaluation.dimension_scores.compliance}/10</td></tr>
                        </table>
                    </div>`;
                });

                document.getElementById('details').innerHTML = html;
            }

            // 初始化
            renderSummary();
            renderDetails();
        </script>
    </body>
    </html>
    """

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == "__main__":
    main()