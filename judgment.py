import re
from typing import List, Tuple


class ContentSafetyChecker:
    def __init__(self):
        # 基础关键词库（需要定期维护更新）
        self.keyword_blacklist = {
            '暴力': ['杀', '打死', '爆炸', '恐怖袭击', '砍人'],
            '色情': ['裸体', '包夜', '卖淫', '色情', '强奸'],
            '违法': ['毒品', '走私', '黑社会', '赌博', '诈骗'],
            '仇恨': ['去死', '人渣', '杂种', '垃圾', '灭绝']
        }

        # 构建正则表达式模式
        self.patterns = {
            category: re.compile('|'.join([re.escape(word) for word in words]))
            for category, words in self.keyword_blacklist.items()
        }

    def check_text(self, text: str) -> Tuple[bool, List[str]]:
        """检查文本是否包含危险内容
        返回：(是否危险, 危险类型列表)"""
        found_categories = []

        # 关键词匹配
        for category, pattern in self.patterns.items():
            if pattern.search(text.lower()):
                found_categories.append(category)

        # 简单语义规则示例
        if self._check_threat(text):
            found_categories.append('暴力威胁')

        return (len(found_categories) > 0, found_categories)

    def _check_threat(self, text: str) -> bool:
        """检查是否包含人身威胁"""
        threat_indicators = [
            r'弄死你?们?',
            r'杀你?全家',
            r'等着瞧',
            r'不得好死'
        ]
        return any(re.search(pattern, text) for pattern in threat_indicators)

    def insert_text(self, test_texts):
        """用于输入文本程序"""
        is_dangerous, categories = self.check_text(test_texts)
        if is_dangerous:
            return f"文本：'{test_texts}'\n危险：{is_dangerous} 类型：{categories}\n"
        else:
            return f"文本：'{test_texts}'\n危险：{is_dangerous} 类型：无类型\n"


# 使用示例
if __name__ == "__main__":
    checker = ContentSafetyChecker()

    test_texts = [
        "你这个垃圾应该去死",
        "今晚一起看电影吗？",
        "我知道怎么制作炸弹",
        "正规商品促销中"
    ]
