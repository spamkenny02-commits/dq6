"""Manual layout for genuine fragments and native three-row choices.
No column-zero auto-wrap. Composite tests must exercise original AE returns.
"""
import re
def compile_fixed(d,source,rev,punct,allowed,widths):
 original=source['tokens'];plan=d['native_plan'].translate(punct)
 tags=[int(x,16) for x in re.findall(r'\{([A-F0-9]{2})\}',plan)]
 assert all(t in allowed|{0xad,0xaf} for t in tags)
 assert [t for t in tags if t not in [0xad,0xaf]]==[t for t in original if t<0x200 and t not in [0xad,0xaf,0xac,0xae]]
 assert tags.count(0xaf)==original.count(0xaf)
 if 1312<=source['id']<=1325:assert tags.count(0xad)==original.count(0xad),(source['id'],'choice line boundaries changed')
 plan=re.sub(r'\{([A-F0-9]{2})\}',lambda m:chr(0xe000+int(m[1],16)),plan)
 tokens=[]
 for c in plan:
  if 0xe000<=ord(c)<0xe200:tokens.append(ord(c)-0xe000)
  else:assert c in rev,(source['id'],c);tokens.append(rev[c])
 tokens.append(original[-1]);lines=plan.split(chr(0xe0ad))
 def width(s):return sum(widths.get(ord(c)-0xe000,0) if 0xe000<=ord(c)<0xe200 else 1 for c in s)
 assert max(map(width,lines))<=24,(source['id'],lines)
 return dict(id=source['id'],tokens=tokens,text=''.join(lines),lines=lines,method='native_fixed_layout_reviewed',source_terminator=original[-1],original_af_count=original.count(0xaf))
