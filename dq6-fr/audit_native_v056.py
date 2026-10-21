"""Reproducible exact-byte caller audit; no inferred natural-play validation."""
from pathlib import Path
import json,hashlib,importlib.util,struct
D=Path(__file__).resolve().parent;R=D.parent;O=D/'v0.56';B=D/'v0.55';read=lambda p:json.loads(p.read_text());source=(R/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes();assert hashlib.sha256(source).hexdigest()=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e'
spec=importlib.util.spec_from_file_location('patch',D/'upstream/refill/patchRM.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);(B/'result.sfc').write_bytes(bytes(p.apply_bps(source,(R/'patches/DQVI-FR-DS-v0.55-BASE-JP-PARTIEL.bps').read_bytes())))
checks=[]
def check(a,h,note):
 b=bytes.fromhex(h);assert source[a:a+len(b)]==b,(hex(a),'source instruction mismatch');checks.append(dict(file_offset=a,cpu_address=0xc00000+a,bytes=b.hex(),meaning=note))
check(0x90910,'22c22dc09817200c0a9011','Show6040; JSR090A0C choice branch.')
check(0x9091b,'22c22dc0991722502ec9003d7e02000060','Show6041; native setbits helper at7E3D00 mask0002; RTS.')
check(0x9092c,'22c22dc09a1722932ec9003d7e02000060','Show6042; native clearbits helper at7E3D00 mask0002; RTS.')
check(0x5907d,'088bf47e7eabab9c516eaf003d7e290200f00bad4058292000f003ee516eab286b','Read3D00 bit2 plus5840 bit20; reset/set6E51, preserving DB/status. Input bit physical button deliberately unnamed.')
check(0x9096a,'22c22dc09e17200c0a9011','Show6046 and choice.')
check(0x90975,'22c22dc09f1722502ec9003d7e04000060','Show6047 then set3D00 bit4.')
check(0x90986,'22c22dc0a01722932ec9003d7e04000060','Show6048 then clear3D00 bit4.')
check(0x254b,'af003d7e290400f017affeffc1101122932ec9013d7e010000a901005ce08cc0','Start-floor conditional bit4; conditional clear3D01 bit1, literal floor1 to C08CE0. No named debug location inferred.')
check(0xdfaf2,'00281822cc99c5b0034c22fb','Text6184 followed by native choice; no jumps to invented DS object meanings.')
check(0xdfb1c,'0029184c25fb002a186b','Yes continuation6185 and no continuation6186.')
check(0xe7444,'2248b6c7223c74ce6b','Yes-poem path calls same C7B648 as fusion prompt, then CE743C.')
check(0xdfb93,'00311822cc99c5b0034cbbfb2248b6c722076dcfa908000c5e3d22a05ec9a9a00022ee8cc0','6193 yes invokes C7B648, sets3D5E bit8, calls map00A0; no equating with simple party join.')
check(0xdfbbb,'00321822cc99c5b0034c06fc22076dcfa910000c723d','6194 yes sets3D72 bit10.')
check(0xdfbd1,'a914028d8e5e','6194 destination map0214.')
check(0xdfc06,'00331822cc99c5b0034c4bfc22076dcfa92b018d8e5e','6195 yes destination map012B.')
check(0x3c5be,'227799c54216c006009003823c00','Show5698 then choose short list when count<6.')
check(0x3c5e4,'c00200f008227799c543168006227799c54416','Short-list third-name layout uses5700; other names5699.')
check(0x3c5ff,'227799c54716','Short-list suffix5703.')
check(0x3c620,'c00200f00dc00400f010227799c543168014227799c54416800c227799c54316227799c54516','Long-list special branches for third/fifth name; after fifth show5701.')
check(0x3c64e,'227799c54616','Long-list suffix5702.')
proof=read(B/'qa-frontiere-6956.json');assert proof['trace'][43]['end']==[0x3b8702,7] and proof['trace'][43]['token']==0xaf
save=lambda n,x:(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
save('qa-appels-natifs.json',dict(source_sha256=hashlib.sha256(source).hexdigest(),checks=checks,verified_caller_bytes=True,debug_context=dict(walking_cancel_bit='7E3D00:0002',debug_start_floor_bit='7E3D00:0004',poem_yes_continuation=6185,poem_no_continuation=6186,fusion_prompt_map='00A0',drop_prompt_map='0214',turn_prompt_map='012B'),equipment_logic=dict(no_users=5704,prefix=5698,short_list_counts=[1,2,3,4,5],short_name_break_after=[3],short_suffix=5703,long_list_counts=[6,7,8],long_name_break_after=[3],conjunction_after=5,long_suffix=5702),limits='Static exact bytes checked against intact source; native inputs/helpers separately tested in private fixtures. Does not prove natural movement, full debug transition, equipment shop/inventory operation or Tulipe scene. Opaque/punning words deliberately remain opaque in French.'))
save('qa-reparation-frontiere.json',dict(id=6956,source_trace_reference='v0.55/qa-frontiere-6956.json',retained_source_prefix_tokens=44,original_final_AF_preserved=True,source_end_exclusive='0x3B8703',added_terminator='AC',original_AC_not_claimed=True,source_garbage_beyond_boundary_not_translated=True,source_extractor_unchanged=True,limits='Explicit safe terminator repair tested by full redecoding and dialogue capture, not proof of original native last-scene termination.'))
print('20 exact caller spans verified; boundary repair explicit')
