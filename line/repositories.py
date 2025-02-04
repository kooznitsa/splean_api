from collections import Counter
import re

from line.lists import stop_words
from line.models import Line


class LineRepository:
    @staticmethod
    def get_frequent_words():
        res = []
        for line in Line.objects.all():
            line = map(lambda x: re.sub(r'\W+', '', x), line.line.lower().split())
            line = filter(lambda x: x not in stop_words.STOP_WORDS, line)
            res.extend(line)
        return dict(Counter(res).most_common(100))
