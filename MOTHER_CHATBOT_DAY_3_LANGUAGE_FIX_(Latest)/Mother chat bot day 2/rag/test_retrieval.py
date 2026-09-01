import json
from backend.retriever import Retriever
from backend.emotion_baseline import analyze
from backend.query_builder import build_query

tests=[
("I got first position today.","achievement"),
("I failed my exam and I feel terrible.","failure"),
("I feel very lonely tonight.","loneliness"),
("I am stressed about tomorrow's presentation.","stress"),
("I am angry with my friend.","anger"),
("I am scared about my results.","fear"),
("Thank you for listening to me.","gratitude"),
("I don't know what I should do.","advice"),
("How can I encourage a child after a mistake?","parenting"),
("My child keeps comparing themselves to classmates.","comparison"),
]*4
r=Retriever()
for i,(msg,label) in enumerate(tests,1):
    a=analyze(msg); q=build_query(msg,a); rows=r.search(q)
    print(f"{i:02d} | expected={label} | emotion={a['emotion']} | top={rows[0]['chunk_id'] if rows else 'NONE'}")
