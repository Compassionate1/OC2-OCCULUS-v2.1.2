import math, random
from .contracts import new_event

def circular_error(a,b):
    return (a-b+180)%360-180

def simulate(seed=2026,steps=120,objects=3):
    rng=random.Random(seed)
    for tick in range(steps):
        for track in range(objects):
            true_bearing=(35+track*90+tick*(0.7+track*.12))%360
            snr=round(rng.uniform(-8,26),3)
            occluded=rng.random()<0.2
            in_view=abs(circular_error(true_bearing,0))<=55
            sigma=max(1.0,16.0/(1+max(snr,0)/10))
            audible=rng.random()<max(.05,min(.98,(snr+10)/38))
            if audible:
                ambiguous=rng.random()<0.12
                measured=(180-true_bearing if ambiguous else true_bearing)+rng.gauss(0,sigma)
                yield new_event('oc2-sim','simulation','audio',{'track_id':f'sim-track-{track+1:03d}','tick':tick,'snr_db':snr,'front_back_ambiguous':ambiguous,'ground_truth_deg':true_bearing},round(measured%360,4),round(max(.05,min(.99,(snr+10)/38)),3))
            if in_view and not occluded:
                measured=(true_bearing+rng.gauss(0,1.8))%360
                yield new_event('oc2-sim','simulation','visual',{'track_id':f'sim-track-{track+1:03d}','tick':tick,'occluded':False,'ground_truth_deg':true_bearing},round(measured,4),0.93)
            elif in_view:
                yield new_event('oc2-sim','simulation','attention',{'track_id':f'sim-track-{track+1:03d}','tick':tick,'occluded':True,'ground_truth_deg':true_bearing},round(true_bearing,4),0.0)
