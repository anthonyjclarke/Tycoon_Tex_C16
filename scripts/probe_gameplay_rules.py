#!/usr/bin/env python3
"""Probe isolated original routines in VICE without modifying game instructions.

A short caller in free workspace invokes the routine with controlled state.
This verifies selected arithmetic behavior, not complete gameplay or timing.
"""

import argparse
import json
import re
from pathlib import Path

from restore_c16 import ROOT, digest
from verify_vice import run_monitor


def probe(build):
    build = build.resolve()
    labels = {n: int(a,16) for a,n in re.findall(r'^al ([0-9A-Fa-f]+) \.(\w+)$',
                                               (build/'tycoon.labels').read_text(),re.M)}
    output = build/'rule-probes'
    output.mkdir(parents=True,exist_ok=True)
    def call(name, program, symbol, accumulator, fields, score=None):
        address=labels[symbol]
        capture=output/(name+'.bin')
        capture.unlink(missing_ok=True)
        # SEI; CLD; LDA #value; JSR routine; NOP. The source reserves no
        # memory at $0500; this caller does not alter any game instruction.
        caller=[0x78,0xD8,0xA9,accumulator,0x20,address&255,address>>8,0xEA]
        commands=f'load "{program}" 0\n'
        for symbol,value in fields.items():commands+=f'> {labels[symbol]:x} {value:02x}\n'
        if score is not None:commands+='> c56 '+' '.join(f'{b:02x}' for b in score.encode('ascii'))+'\n'
        commands+='> 500 '+' '.join(f'{b:02x}' for b in caller)+'\nbreak 507\ng 500\n'
        commands+=f'bsave "{capture}" 0 0000 3fff\nquit\n'
        log=run_monitor(output,name,commands)
        if 'c:$0507' not in log.lower():raise ValueError('Probe did not return to its caller')
        data=capture.read_bytes()
        return data
    source=build/'tycoon-tex.prg'
    ref_data=(build/'reference-memory.bin').read_bytes()
    if len(ref_data)!=0x3000:raise ValueError('Run verify_vice.py before probing the packed reference')
    reference=output/'reference-unpacked.prg'
    reference.write_bytes(b'\x00\x10'+ref_data)
    checks=[]
    for name,path in [('source',source),('running-reference',reference)]:
        mem=call('score-'+name,path,'SCORE',1,{'LIVES':3,'XTRA':0},'000999')
        result={'probe':'score-999-plus-1','version':name,'score':mem[0xC56:0xC5C].decode('ascii'),
                'lives':mem[labels['LIVES']],'cached_digit':mem[labels['XTRA']]}
        assert result['score']=='001000'
        assert result['lives']==(4 if name=='source' else 3)
        checks.append(result)
    mem=call('pressure-crossing',source,'PRESDO',4,{'PRESHI':10,'PRESLO':1,'BLOOUT':0})
    result={'probe':'pressure-crossing','before_hi':10,'before_lo':1,'amount':4,
            'after_hi':mem[labels['PRESHI']],'after_lo':mem[labels['PRESLO']],
            'blowout':mem[labels['BLOOUT']]}
    assert (result['after_hi'],result['after_lo'],result['blowout'])==(9,7,0)
    checks.append(result)
    mem=call('completion-crossing',source,'COMPUP',1,{'COMPHI':25,'COMPLO':7,'DONE':0})
    result={'probe':'completion-crossing','before_hi':25,'before_lo':7,'amount':1,
            'after_hi':mem[labels['COMPHI']],'after_lo':mem[labels['COMPLO']],
            'done':mem[labels['DONE']]}
    assert (result['after_hi'],result['after_lo'],result['done'])==(26,0,0)
    checks.append(result)
    mem=call('completion-followup',source,'COMPUP',1,{'COMPHI':26,'COMPLO':0,'DONE':0})
    assert mem[labels['DONE']]==1
    checks.append({'probe':'completion-followup','before_hi':26,'before_lo':0,'amount':1,
                   'after_hi':mem[labels['COMPHI']],'after_lo':mem[labels['COMPLO']],
                   'done':mem[labels['DONE']]})
    report={'method':'isolated routine calls using a workspace caller; SEI/CLD; controlled RAM; original game instructions unchanged',
            'source_prg_sha256':digest(source.read_bytes()),
            'reference_memory_sha256':digest(ref_data),'emulator':'VICE xplus4, PAL C16, 16 KB',
            'scope':'five arithmetic observations; not full gameplay, concurrency, overflow or sound verification',
            'checks':checks}
    (output/'rule-probes.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir',type=Path,default=ROOT/'build')
    probe(parser.parse_args().build_dir)
