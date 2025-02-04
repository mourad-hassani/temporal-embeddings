from typing import Tuple, List

def contains_temporal_expression(text: str, client) -> Tuple[bool, List[str]]:
    temporal_expression_bool = False
    temporal_expressions = []
    
    doc = client.annotate(text)
    
    for sentence in doc.sentence:
        for token in sentence.token:
            if token.ner in ["DATE", "TIME", "DURATION", "SET"]:
                if not token.timexValue.text in [e.text for e in temporal_expressions]:
                    temporal_expression_bool = True
                    temporal_expressions.append(token.timexValue)
    
    return temporal_expression_bool, temporal_expressions