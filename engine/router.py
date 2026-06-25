"""Router — situation-triage logic.

Analyzes free-form user text, identifies intent, extracts structured info,
and routes to the right combination of skills.
"""

import yaml
import json
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "skills" / "data"

# Load methodology data (contains intent keywords + crisis signals)
def _load_yaml(filename):
    filepath = _DATA_DIR / filename
    if not filepath.exists():
        return {}
    with open(filepath, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

_METHODOLOGY = _load_yaml("methodology-tools.yaml")
_MARXISM_TOOLS = _load_yaml("marxism-tools.yaml")
_DENG_TOOLS = _load_yaml("deng-tools.yaml")
_XI_TOOLS = _load_yaml("xi-tools.yaml")
_INDUSTRY = _load_yaml("industry-signals.yaml")
_REGIONAL = _load_yaml("regional-matrix.yaml")
# 产业链卡点分析工具（Serenity 方法·战略库第二根源）
_CHAIN = _load_yaml("industrial-chain-tools.yaml")
# 经济政策推演方法（战略库第三根源·Phase 2 方法框架·evergreen）
_DEDUCTION = _load_yaml("policy-deduction-tools.yaml")
# 逐集群行业前景卡片（战略库第三根源·09 行业前景推演蒸馏·evergreen）
_FORECAST = _load_yaml("industry-forecast-tools.yaml")

# Industry keyword -> cluster mapping
_INDUSTRY_KEYWORDS = {
    # A
    "集成电路": "A-先进制造与硬科技", "半导体": "A-先进制造与硬科技", "芯片": "A-先进制造与硬科技",
    "工业母机": "A-先进制造与硬科技", "数控": "A-先进制造与硬科技", "cnc": "A-先进制造与硬科技",
    "高端装备": "A-先进制造与硬科技", "新材料": "A-先进制造与硬科技", "基础软件": "A-先进制造与硬科技",
    "生物制造": "A-先进制造与硬科技", "嵌入式": "A-先进制造与硬科技", "硬件": "A-先进制造与硬科技",
    # B
    "人工智能": "B-数字与智能产业", "ai": "B-数字与智能产业", "算力": "B-数字与智能产业",
    "软件开发": "B-数字与智能产业", "编程": "B-数字与智能产业", "程序员": "B-数字与智能产业",
    "数据": "B-数字与智能产业", "工业互联网": "B-数字与智能产业", "平台": "B-数字与智能产业",
    "前端": "B-数字与智能产业", "后端": "B-数字与智能产业", "java": "B-数字与智能产业",
    "python": "B-数字与智能产业", "互联网": "B-数字与智能产业",
    # C
    "光伏": "C-绿色能源全链", "风电": "C-绿色能源全链", "水电": "C-绿色能源全链",
    "核电": "C-绿色能源全链", "储能": "C-绿色能源全链", "电网": "C-绿色能源全链",
    "碳": "C-绿色能源全链", "氢能": "C-绿色能源全链", "新能源": "C-绿色能源全链",
    "电力": "C-绿色能源全链", "电气": "C-绿色能源全链", "电工": "C-绿色能源全链",
    # D
    "农业": "D-农业与乡村振兴", "种植": "D-农业与乡村振兴", "养殖": "D-农业与乡村振兴",
    "种业": "D-农业与乡村振兴", "农机": "D-农业与乡村振兴", "农技": "D-农业与乡村振兴",
    "农产品": "D-农业与乡村振兴", "农村": "D-农业与乡村振兴",
    # E
    "养老": "E-民生服务", "银发": "E-民生服务", "托育": "E-民生服务", "育婴": "E-民生服务",
    "医疗": "E-民生服务", "健康": "E-民生服务", "护理": "E-民生服务", "护士": "E-民生服务",
    "创新药": "E-民生服务", "家政": "E-民生服务", "医药": "E-民生服务",
    # F
    "网文": "F-文化创意与出海", "游戏": "F-文化创意与出海", "影视": "F-文化创意与出海",
    "短剧": "F-文化创意与出海", "动漫": "F-文化创意与出海", "文化": "F-文化创意与出海",
    "内容创作": "F-文化创意与出海", "出海": "F-文化创意与出海",
    # G
    "交通": "G-基建物流房地产", "物流": "G-基建物流房地产", "快递": "G-基建物流房地产",
    "建筑": "G-基建物流房地产", "房地产": "G-基建物流房地产", "物业": "G-基建物流房地产",
    "低空": "G-基建物流房地产", "无人机": "G-基建物流房地产", "外卖": "G-基建物流房地产",
    "骑手": "G-基建物流房地产", "配送": "G-基建物流房地产",
    # H
    "机器人": "H-新兴未来产业", "具身智能": "H-新兴未来产业", "商业航天": "H-新兴未来产业",
    "量子": "H-新兴未来产业", "聚变": "H-新兴未来产业", "6g": "H-新兴未来产业",
    # I
    "煤矿": "I-传统矿业与资源开采", "矿业": "I-传统矿业与资源开采", "矿工": "I-传统矿业与资源开采",
    "油气": "I-传统矿业与资源开采", "金属矿": "I-传统矿业与资源开采",
    # J
    "纺织": "J-传统轻纺与日用制造", "服装": "J-传统轻纺与日用制造", "食品饮料": "J-传统轻纺与日用制造",
    "家具": "J-传统轻纺与日用制造", "玩具": "J-传统轻纺与日用制造", "鞋帽": "J-传统轻纺与日用制造",
    # K
    "钢铁": "K-传统重化工与建材", "水泥": "K-传统重化工与建材", "化工": "K-传统重化工与建材",
    "玻璃": "K-传统重化工与建材", "陶瓷": "K-传统重化工与建材", "有色冶炼": "K-传统重化工与建材",
    # L
    "零售": "L-商贸零售与餐饮住宿", "超市": "L-商贸零售与餐饮住宿", "便利店": "L-商贸零售与餐饮住宿",
    "电商": "L-商贸零售与餐饮住宿", "餐饮": "L-商贸零售与餐饮住宿", "酒店": "L-商贸零售与餐饮住宿",
    "民宿": "L-商贸零售与餐饮住宿", "旅游": "L-商贸零售与餐饮住宿", "百货": "L-商贸零售与餐饮住宿",
    # M
    "银行": "M-金融与商务服务", "保险": "M-金融与商务服务", "证券": "M-金融与商务服务",
    "法律": "M-金融与商务服务", "会计": "M-金融与商务服务", "咨询": "M-金融与商务服务",
    "广告": "M-金融与商务服务", "财务": "M-金融与商务服务",
    # N
    "教育": "N-教育与培训", "教培": "N-教育与培训", "培训": "N-教育与培训",
    "老师": "N-教育与培训", "教师": "N-教育与培训", "教学": "N-教育与培训",
    # O
    "美容": "O-居民生活服务", "美发": "O-居民生活服务", "理发": "O-居民生活服务",
    "修理": "O-居民生活服务", "宠物": "O-居民生活服务", "健身": "O-居民生活服务",
    "婚庆": "O-居民生活服务", "汽修": "O-居民生活服务", "维修": "O-居民生活服务",
    # P
    "环卫": "P-公用事业与市政服务", "供水": "P-公用事业与市政服务", "燃气": "P-公用事业与市政服务",
    "市政": "P-公用事业与市政服务", "环保": "P-公用事业与市政服务", "公交": "P-公用事业与市政服务",
}

# Region keyword mapping
_REGION_KEYWORDS = {
    "①三大动力源": [
        "北京", "上海", "深圳", "广州", "杭州", "苏州", "天津", "南京", "无锡", "宁波",
        "东莞", "佛山", "珠海", "中山", "大湾区", "长三角", "京津冀", "珠三角",
        "宝安", "南山", "福田", "浦东", "海淀", "朝阳",
    ],
    "②新兴增长极": [
        "成都", "重庆", "武汉", "长沙", "合肥", "西安", "郑州", "南昌", "昆明", "贵阳",
        "成渝", "长江中游", "中部",
    ],
    "③战略腹地与西部": [
        "新疆", "西藏", "青海", "甘肃", "宁夏", "内蒙古", "南宁", "兰州", "乌鲁木齐",
        "西部", "西北", "西南",
    ],
    "④东北老工业基地": [
        "黑龙江", "吉林", "辽宁", "哈尔滨", "长春", "沈阳", "大连", "东北",
    ],
    "⑤县域与乡村": [
        "县", "乡镇", "村", "农村", "老家", "返乡", "回乡", "县城",
    ],
}


def triage(situation_text: str) -> dict:
    """Main routing function: analyze user text and return triage result."""
    text_lower = situation_text.lower()

    # Step 1: Crisis check (highest priority)
    crisis_signals = _METHODOLOGY.get("crisis_signals", {})
    crisis_kw = crisis_signals.get("危机", [])
    exhaustion_kw = crisis_signals.get("耗竭", [])

    crisis_hit = [kw for kw in crisis_kw if kw in situation_text]
    exhaustion_hit = [kw for kw in exhaustion_kw if kw in situation_text]

    if crisis_hit:
        return {
            "special_handling": "crisis",
            "message": (
                "检测到情绪危机信号。此时不做任何职业判断。\n"
                "如果你正在经历困难，请拨打24小时心理援助热线：400-161-9995 或北京心理危机研究与干预中心：010-82951332。\n"
                "你不是一个人。状态不对时做的决策不可靠，先照顾好自己。"
            ),
            "route_to": [],
        }

    # Step 2: Intent identification
    intent_keywords = _METHODOLOGY.get("intent_keywords", {})
    detected_intents = []
    for intent, keywords in intent_keywords.items():
        hits = [kw for kw in keywords if kw in situation_text]
        if hits:
            detected_intents.append({"intent": intent, "matched_keywords": hits})

    # Determine routing priority
    route_to = []
    has_exhaustion = bool(exhaustion_hit)
    has_confusion = any(i["intent"] == "困境迷茫" for i in detected_intents)

    if has_exhaustion or has_confusion:
        route_to.append("problem-diagnosis")

    # Add other intents (deduplicated)
    for item in detected_intents:
        skill_map = {
            "困境迷茫": "problem-diagnosis",
            "行业判断": "industry-scan",
            "创业意向": "startup-feasibility",
            "成长需求": "growth-planner",
            "协作需求": "collaboration-match",
            "趋势前瞻": "opportunity-radar",
        }
        skill = skill_map.get(item["intent"])
        if skill and skill not in route_to:
            route_to.append(skill)

    # If no intent detected, check if we at least have an industry → default to industry-scan
    if not route_to:
        # Pre-scan for industry to decide if we can still help
        temp_text_lower = situation_text.lower()
        has_industry = any(kw in temp_text_lower for kw in _INDUSTRY_KEYWORDS)
        if has_industry:
            route_to.append("industry-scan")
        else:
            return {
                "special_handling": "need_more_info",
                "message": (
                    "我想更好地帮你。你能告诉我：\n"
                    "1. 你目前在做什么行业/岗位？\n"
                    "2. 你在哪个城市？\n"
                    "3. 你最想了解什么——行业前景？创业？学习成长？还是遇到了什么困难？"
                ),
                "route_to": [],
            }

    # Step 3: Extract structured info
    extracted = {
        "industry": None,
        "cluster": None,
        "region": None,
        "region_name": None,
        "age": None,
        "finances": None,
        "family": None,
        "emotional_state": "正常",
    }

    # Industry
    for kw, cluster in _INDUSTRY_KEYWORDS.items():
        if kw in text_lower:
            extracted["industry"] = kw
            extracted["cluster"] = cluster
            break

    # Region
    for region, keywords in _REGION_KEYWORDS.items():
        for kw in keywords:
            if kw in situation_text:
                extracted["region"] = region
                extracted["region_name"] = region
                break
        if extracted["region"]:
            break

    # Age
    import re
    age_match = re.search(r'(\d{2})\s*岁', situation_text)
    if age_match:
        extracted["age"] = int(age_match.group(1))

    # Finances
    finance_kw = {"月光": "月光", "负债": "负债", "结余": "有结余", "存款": "有结余",
                  "房贷": "有房贷", "攒": "有结余"}
    for kw, status in finance_kw.items():
        if kw in situation_text:
            extracted["finances"] = status
            break

    # Family
    family_kw = {"妻子": "有伴侣", "老公": "有伴侣", "对象": "有伴侣", "相亲": "有伴侣",
                 "孩子": "有孩子", "父母": "有父母", "单身": "单身", "结婚": "已婚"}
    for kw, status in family_kw.items():
        if kw in situation_text:
            extracted["family"] = status
            break

    # Emotional state
    if exhaustion_hit:
        extracted["emotional_state"] = "耗竭"
    elif any(kw in situation_text for kw in ["焦虑", "压力大", "迷茫"]):
        extracted["emotional_state"] = "焦虑/迷茫"

    # Step 4: Build result
    result = {
        "detected_intents": detected_intents,
        "route_to": route_to,
        "extracted_info": extracted,
    }

    if has_exhaustion:
        result["special_handling"] = "exhaustion"
        result["special_note"] = (
            "检测到明显的疲惫/耗竭信号。重要提醒：在疲惫状态下做重大决策容易后悔。"
            "建议先给自己2-4周「只恢复不决策」的时间——先照顾好自己，再处理职业问题。"
        )

    return result


def get_industry_signal(cluster: str) -> dict:
    """Get industry signal data for a cluster."""
    if not cluster or cluster not in _INDUSTRY:
        return {}
    data = _INDUSTRY[cluster]
    return {
        "cluster": cluster,
        "signal": data.get("signal", "未知"),
        "certainty": data.get("certainty", 0),
        "methodology": data.get("methodology", ""),
        "growth_roles": data.get("growth_roles", []),
        "shrink_roles": data.get("shrink_roles", []),
        "transition_from": data.get("transition_from", []),
        "notes": data.get("notes", ""),
    }


# ── 集群认知框架 ──
_FRAMEWORKS_DIR = Path(__file__).resolve().parent.parent / "methodology" / "cluster_frameworks"


def get_cluster_framework(cluster: str) -> str:
    """Get the cognitive framework text for a cluster.

    Returns the full markdown content of the framework file, or empty string if not found.
    These frameworks connect methodology (伟人思想) to specific industry clusters,
    giving workers a "how to think about your industry" cognitive layer.
    """
    if not cluster:
        return ""
    framework_path = _FRAMEWORKS_DIR / f"{cluster}.md"
    if not framework_path.exists():
        return ""
    return framework_path.read_text(encoding="utf-8")


# ── 马克思主义工具与启发 ──
_MARXISM_INSPIRATION_DIR = Path(__file__).resolve().parent.parent / "methodology" / "marxism" / "inspiration"


def get_marxism_tools_for_cluster(cluster: str) -> list:
    """Get the most relevant marxism thinking tools for a cluster.

    Returns a list of tool dicts with principle, one_liner, quote_source.
    """
    if not cluster:
        return []
    cluster_match = _MARXISM_TOOLS.get("cluster_match", {})
    tool_keys = cluster_match.get(cluster, [])
    all_tools = _MARXISM_TOOLS.get("tools", {})
    result = []
    for key in tool_keys:
        tool = all_tools.get(key, {})
        if tool:
            result.append({
                "name": key,
                "principle": tool.get("principle", ""),
                "one_liner": tool.get("one_liner", ""),
                "use_when": tool.get("use_when", ""),
                "quote_source": tool.get("quote_source", ""),
            })
    return result


def get_marxism_inspiration(situation: str, cluster: str = None, limit: int = 2) -> list:
    """Find the most relevant marxism inspiration files for a given situation.

    Scans the marxism inspiration directory, matches files by keyword relevance
    to the user's situation and cluster.
    Returns a list of {title, excerpt} dicts.
    """
    if not _MARXISM_INSPIRATION_DIR.exists():
        return []

    # Keywords derived from the situation text
    situation_lower = situation.lower() if situation else ""

    # Cluster-specific keyword boost
    cluster_keywords = {
        "A-先进制造与硬科技": ["工厂", "产线", "制造", "设备", "嵌入式", "技能"],
        "B-数字与智能产业": ["程序员", "代码", "AI", "互联网", "算法"],
        "C-绿色能源全链": ["光伏", "风电", "电站", "运维", "电工"],
        "D-农业与乡村振兴": ["农村", "返乡", "种植", "农业", "县城"],
        "E-民生服务": ["养老", "护理", "服务", "人"],
        "F-文化创意与出海": ["内容", "创作", "出海", "短剧"],
        "G-基建物流房地产": ["外卖", "骑手", "快递", "物流", "建筑"],
        "H-新兴未来产业": ["机器人", "无人机", "AI", "新兴"],
        "I-传统矿业与资源开采": ["矿", "矿工"],
        "J-传统轻纺与日用制造": ["纺织", "服装", "工厂"],
        "K-传统重化工与建材": ["钢铁", "水泥", "化工"],
        "L-商贸零售与餐饮住宿": ["店", "零售", "餐饮", "电商"],
        "M-金融与商务服务": ["银行", "金融", "工资", "保险"],
        "N-教育与培训": ["教师", "教育", "学习", "培训"],
        "O-居民生活服务": ["美容", "维修", "宠物", "汽修"],
        "P-公用事业与市政服务": ["环卫", "公交", "司机"],
    }

    scored_files = []
    for f in _MARXISM_INSPIRATION_DIR.rglob("*.md"):
        if f.name in ("README.md", "index.md"):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue

        # Score by keyword matches in title + first 800 chars
        title = f.stem
        excerpt_zone = (title + " " + text[:800]).lower()
        score = 0

        # Situation keyword match — use meaningful 2+ char substrings
        situation_keywords = ["嵌入式", "开发", "深圳", "累", "工资", "前景", "行业",
                              "机器人", "养老", "护理", "外卖", "骑手", "快递", "矿工",
                              "纺织", "钢铁", "水泥", "化工", "程序员", "教师", "教育",
                              "焦虑", "迷茫", "转行", "创业", "开店", "副业", "考证",
                              "学习", "合作", "合伙", "未来", "趋势", "被替代", "AI",
                              "光伏", "风电", "农业", "返乡", "县城", "银行", "餐饮",
                              "汽修", "美容", "宠物", "环卫", "公交", "司机"]
        for word in situation_keywords:
            if word in situation_lower and word in excerpt_zone:
                score += 2

        # Cluster keyword boost
        if cluster and cluster in cluster_keywords:
            for kw in cluster_keywords[cluster]:
                if kw in excerpt_zone:
                    score += 5

        # Emotional state keywords
        for kw in ["累", "穷", "焦虑", "迷茫", "不想干", "压力", "加班", "被替代"]:
            if kw in situation_lower and kw in excerpt_zone:
                score += 3

        if score > 0:
            # Extract first meaningful paragraph as excerpt
            lines = text.split("\n")
            excerpt_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and not stripped.startswith(">") and not stripped.startswith("日期") and not stripped.startswith("原文对应") and not stripped.startswith("说明："):
                    excerpt_lines.append(stripped)
                    if len(excerpt_lines) >= 2:
                        break
            excerpt = " ".join(excerpt_lines)[:300]
            scored_files.append((score, title, excerpt, str(f.relative_to(_MARXISM_INSPIRATION_DIR))))

    scored_files.sort(key=lambda x: x[0], reverse=True)
    return [
        {"title": title, "excerpt": excerpt, "path": path}
        for _, title, excerpt, path in scored_files[:limit]
    ]


# ── 邓小平理论工具与启发 ──
_DENG_INSPIRATION_DIR = Path(__file__).resolve().parent.parent / "methodology" / "deng_xiaoping_theory" / "inspiration"


def get_deng_tools_for_cluster(cluster: str) -> list:
    """Get the most relevant deng xiaoping theory tools for a cluster."""
    if not cluster:
        return []
    cluster_match = _DENG_TOOLS.get("cluster_match", {})
    tool_keys = cluster_match.get(cluster, [])
    all_tools = _DENG_TOOLS.get("tools", {})
    result = []
    for key in tool_keys:
        tool = all_tools.get(key, {})
        if tool:
            result.append({
                "name": key,
                "principle": tool.get("principle", ""),
                "one_liner": tool.get("one_liner", ""),
                "use_when": tool.get("use_when", ""),
                "quote_source": tool.get("quote_source", ""),
            })
    return result


def get_deng_inspiration(situation: str, cluster: str = None, limit: int = 2) -> list:
    """Find the most relevant deng xiaoping theory inspiration files."""
    if not _DENG_INSPIRATION_DIR.exists():
        return []

    situation_lower = situation.lower() if situation else ""

    scored_files = []
    for f in _DENG_INSPIRATION_DIR.rglob("*.md"):
        if f.name in ("README.md", "index.md"):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue

        title = f.stem
        excerpt_zone = (title + " " + text[:800]).lower()
        score = 0

        situation_keywords = ["嵌入式", "开发", "深圳", "累", "工资", "前景", "行业",
                              "机器人", "养老", "护理", "外卖", "骑手", "快递", "矿工",
                              "纺织", "钢铁", "水泥", "化工", "程序员", "教师", "教育",
                              "焦虑", "迷茫", "转行", "创业", "开店", "副业", "考证",
                              "学习", "合作", "合伙", "未来", "趋势", "被替代", "AI",
                              "纠结", "犹豫", "不知道", "怎么选", "准备"]
        for word in situation_keywords:
            if word in situation_lower and word in excerpt_zone:
                score += 2

        emotional_kw = ["累", "穷", "焦虑", "迷茫", "不想干", "压力", "加班", "被替代",
                        "纠结", "犹豫", "害怕", "不敢"]
        for kw in emotional_kw:
            if kw in situation_lower and kw in excerpt_zone:
                score += 3

        if score > 0:
            lines = text.split("\n")
            excerpt_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and not stripped.startswith(">") and not stripped.startswith("日期") and not stripped.startswith("原文对应") and not stripped.startswith("说明："):
                    excerpt_lines.append(stripped)
                    if len(excerpt_lines) >= 2:
                        break
            excerpt = " ".join(excerpt_lines)[:300]
            scored_files.append((score, title, excerpt, str(f.relative_to(_DENG_INSPIRATION_DIR))))

    scored_files.sort(key=lambda x: x[0], reverse=True)
    return [
        {"title": title, "excerpt": excerpt, "path": path}
        for _, title, excerpt, path in scored_files[:limit]
    ]


# ── 毛泽东 / 习近平启发库（带缓存的实时检索）──
# 毛泽东启发库有 1500+ 篇，逐请求读盘代价高，因此用模块级缓存：
# 每个目录只在首次检索时读盘一次，之后在内存中按情境打分。
_MAO_INSPIRATION_DIR = Path(__file__).resolve().parent.parent / "methodology" / "mao_zedong_thought" / "inspiration"
_XI_INSPIRATION_DIR = Path(__file__).resolve().parent.parent / "methodology" / "xi_jinping_thought" / "inspiration"

_INSPIRATION_CACHE = {}


def _load_inspiration_dir(base_dir):
    """懒加载并缓存某启发库目录下所有文件的 (title, zone, excerpt, relpath)。

    zone = 小写的「标题 + 正文前 800 字」，用于关键词打分；
    excerpt = 前两段有意义的正文，用于展示。
    """
    key = str(base_dir)
    if key in _INSPIRATION_CACHE:
        return _INSPIRATION_CACHE[key]
    entries = []
    if base_dir.exists():
        for f in base_dir.rglob("*.md"):
            if f.name in ("README.md", "index.md"):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            title = f.stem
            zone = (title + " " + text[:800]).lower()
            excerpt_lines = []
            for line in text.split("\n"):
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and not stripped.startswith(">") and not stripped.startswith("日期") and not stripped.startswith("原文对应") and not stripped.startswith("说明："):
                    excerpt_lines.append(stripped)
                    if len(excerpt_lines) >= 2:
                        break
            excerpt = " ".join(excerpt_lines)[:300]
            entries.append((title, zone, excerpt, str(f.relative_to(base_dir))))
    _INSPIRATION_CACHE[key] = entries
    return entries


def _score_cached_inspiration(base_dir, situation, cluster, limit):
    """从缓存的启发库条目里，按情境/集群/情绪关键词选出最相关的几篇。

    打分口径与 get_marxism_inspiration 一致（含集群关键词加权）。
    """
    situation_lower = situation.lower() if situation else ""
    cluster_keywords = {
        "A-先进制造与硬科技": ["工厂", "产线", "制造", "设备", "嵌入式", "技能"],
        "B-数字与智能产业": ["程序员", "代码", "AI", "互联网", "算法"],
        "C-绿色能源全链": ["光伏", "风电", "电站", "运维", "电工"],
        "D-农业与乡村振兴": ["农村", "返乡", "种植", "农业", "县城"],
        "E-民生服务": ["养老", "护理", "服务", "人"],
        "F-文化创意与出海": ["内容", "创作", "出海", "短剧"],
        "G-基建物流房地产": ["外卖", "骑手", "快递", "物流", "建筑"],
        "H-新兴未来产业": ["机器人", "无人机", "AI", "新兴"],
        "I-传统矿业与资源开采": ["矿", "矿工"],
        "J-传统轻纺与日用制造": ["纺织", "服装", "工厂"],
        "K-传统重化工与建材": ["钢铁", "水泥", "化工"],
        "L-商贸零售与餐饮住宿": ["店", "零售", "餐饮", "电商"],
        "M-金融与商务服务": ["银行", "金融", "工资", "保险"],
        "N-教育与培训": ["教师", "教育", "学习", "培训"],
        "O-居民生活服务": ["美容", "维修", "宠物", "汽修"],
        "P-公用事业与市政服务": ["环卫", "公交", "司机"],
    }
    situation_keywords = ["嵌入式", "开发", "深圳", "累", "工资", "前景", "行业",
                          "机器人", "养老", "护理", "外卖", "骑手", "快递", "矿工",
                          "纺织", "钢铁", "水泥", "化工", "程序员", "教师", "教育",
                          "焦虑", "迷茫", "转行", "创业", "开店", "副业", "考证",
                          "学习", "合作", "合伙", "未来", "趋势", "被替代", "AI",
                          "光伏", "风电", "农业", "返乡", "县城", "银行", "餐饮",
                          "汽修", "美容", "宠物", "环卫", "公交", "司机"]
    emotional_kw = ["累", "穷", "焦虑", "迷茫", "不想干", "压力", "加班", "被替代"]

    scored = []
    for title, zone, excerpt, relpath in _load_inspiration_dir(base_dir):
        score = 0
        for word in situation_keywords:
            if word in situation_lower and word in zone:
                score += 2
        if cluster and cluster in cluster_keywords:
            for kw in cluster_keywords[cluster]:
                if kw in zone:
                    score += 5
        for kw in emotional_kw:
            if kw in situation_lower and kw in zone:
                score += 3
        if score > 0:
            scored.append((score, title, excerpt, relpath))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"title": t, "excerpt": e, "path": p} for _, t, e, p in scored[:limit]]


def get_mao_inspiration(situation: str, cluster: str = None, limit: int = 2) -> list:
    """Find the most relevant Mao Zedong thought inspiration files (cached)."""
    return _score_cached_inspiration(_MAO_INSPIRATION_DIR, situation, cluster, limit)


def get_xi_inspiration(situation: str, cluster: str = None, limit: int = 2) -> list:
    """Find the most relevant Xi Jinping thought inspiration files (cached)."""
    return _score_cached_inspiration(_XI_INSPIRATION_DIR, situation, cluster, limit)


# ── 习近平思想工具 ──

def get_xi_tools_for_cluster(cluster: str) -> list:
    """Get the most relevant xi jinping thought tools for a cluster."""
    if not cluster:
        return []
    cluster_match = _XI_TOOLS.get("cluster_match", {})
    tool_keys = cluster_match.get(cluster, [])
    all_tools = _XI_TOOLS.get("tools", {})
    result = []
    for key in tool_keys:
        tool = all_tools.get(key, {})
        if tool:
            result.append({
                "name": key,
                "principle": tool.get("principle", ""),
                "one_liner": tool.get("one_liner", ""),
                "use_when": tool.get("use_when", ""),
                "quote_source": tool.get("quote_source", ""),
            })
    return result


# ── 产业链卡点分析工具（Serenity 方法·战略库第二根源）──

def get_chain_tools_for_cluster(cluster: str) -> list:
    """Get the most relevant industrial-chain (Serenity 方法) tools for a cluster.

    Returns a list of tool dicts with principle, one_liner, use_when, quote_source.
    """
    if not cluster:
        return []
    cluster_match = _CHAIN.get("cluster_match", {})
    tool_keys = cluster_match.get(cluster, [])
    all_tools = _CHAIN.get("tools", {})
    result = []
    for key in tool_keys:
        tool = all_tools.get(key, {})
        if tool:
            result.append({
                "name": key,
                "principle": tool.get("principle", ""),
                "one_liner": tool.get("one_liner", ""),
                "use_when": tool.get("use_when", ""),
                "quote_source": tool.get("quote_source", ""),
            })
    return result


def get_policy_deduction_method() -> dict:
    """Get the evergreen economic-policy deduction method (six steps + honest boundaries).

    Universal macro-forecasting method distilled from strategy/economic_policy/06 —
    NOT cluster-specific. Returns {} if the data file is missing or empty.
    """
    if not _DEDUCTION:
        return {}
    steps = _DEDUCTION.get("method_steps", [])
    boundaries = _DEDUCTION.get("honest_boundaries", [])
    if not steps and not boundaries:
        return {}
    return {"method_steps": steps, "honest_boundaries": boundaries}


def get_industry_forecast_for_cluster(cluster: str) -> dict:
    """Get the evergreen per-cluster industry-forecast card.

    Distilled from strategy/economic_policy/09-行业前景推演/<cluster>.md — slow-moving
    fields only (main_issue/tone/positioning/watch_indicators/one_liner/source); the
    time-sensitive specifics live in the knowledge file pointed to by `source`.
    Returns {} if cluster is empty or has no card.
    """
    if not cluster:
        return {}
    forecasts = _FORECAST.get("forecasts", {})
    card = forecasts.get(cluster, {})
    if not card:
        return {}
    return {
        "main_issue": card.get("main_issue", ""),
        "tone": card.get("tone", ""),
        "positioning": card.get("positioning", ""),
        "watch_indicators": card.get("watch_indicators", ""),
        "one_liner": card.get("one_liner", ""),
        "source": card.get("source", ""),
    }


def get_regional_score(opportunity: str, region: str) -> int:
    """Get the opportunity score for a region from the matrix."""
    matrix = _REGIONAL.get("opportunity_matrix", {})
    opp_data = matrix.get(opportunity, {})
    region_key = region[0] if region else None  # First char: ①②③④⑤
    if region_key and region_key in opp_data:
        return opp_data[region_key]
    return 0


def assess_completeness(info: dict, route_to: list) -> dict:
    """Assess how complete the user's information is for the routed skills.

    Returns a dict with:
    - ready: bool — enough info to analyze
    - completeness_pct: 0-100
    - missing_fields: list of field names that are missing
    - next_question: the single most important question to ask next
    """
    # Define which fields each skill needs
    skill_needs = {
        "problem-diagnosis": [],  # works with free text, no required fields
        "industry-scan": ["cluster", "region"],
        "startup-feasibility": ["finances", "family"],
        "growth-planner": ["age"],
        "collaboration-match": [],
        "opportunity-radar": [],
        "situation-triage": [],
    }

    # Collect all missing fields across routed skills
    missing = []
    for skill in route_to:
        for field in skill_needs.get(skill, []):
            if not info.get(field) and field not in missing:
                missing.append(field)

    # Calculate completeness
    total_possible = len({"cluster", "region", "age", "finances", "family", "industry"})
    filled = sum(1 for f in ["cluster", "region", "age", "finances", "family", "industry"] if info.get(f))
    pct = int(filled / total_possible * 100)

    # For problem-diagnosis-only routes, don't require extra fields
    if route_to == ["problem-diagnosis"] or not route_to:
        ready = True
        missing = []
    else:
        # Ready if no critical fields missing AND not too many fields missing overall.
        # Critical = cluster/region (for industry-scan).
        # For startup-feasibility, finances+family matter for abort checks,
        # so allow at most 1 missing field before requiring more questions.
        critical = [f for f in missing if f in ("cluster", "region")]
        ready = len(critical) == 0 and len(missing) <= 1

    # Determine the single next question (priority order)
    next_question = None
    question_map = {
        "cluster": "你目前在做什么工作？不用很正式，说说你平时主要干些什么就行。",
        "region": "你在哪个地方？不同城市差别还挺大的，我帮你看看你那边的情况。",
        "age": "方便告诉我你大概多大了吗？不同年纪，能走的路确实不太一样。",
        "finances": "现在经济上压力大不大？比如有没有攒下一点备用金？这个会影响我给你的建议。",
        "family": "家里人对你现在想的事是什么态度？他们的支持挺重要的。",
    }
    for field in ["cluster", "region", "age", "finances", "family"]:
        if field in missing:
            next_question = question_map[field]
            break

    return {
        "ready": ready,
        "completeness_pct": pct,
        "missing_fields": missing,
        "next_question": next_question,
    }
