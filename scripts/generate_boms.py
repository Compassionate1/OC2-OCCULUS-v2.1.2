#!/usr/bin/env python3
"""Deterministic source-level SBOM and CBOM; does not claim resolved transitive dependencies."""
import json,hashlib,re,sys,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'compliance'; OUT.mkdir(exist_ok=True)
VERSION='2.0.3.0'

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def ref(name,version): return 'pkg:'+name+'@'+version
# Source declarations, not a lockfile or container runtime inspection.
items=[
 ('OC2-OCCULUS','2.0.3.0','application','source','NOASSERTION'),
 ('bop5ii','1.0.0','library','research-python/pyproject.toml','MIT'),
 ('OCCULUSCore','2.0.3.0','library','Package.swift','NOASSERTION'),
 ('kafka-python','2.0.2','library','infra/gateway/Dockerfile','NOASSERTION'),
 ('psycopg[binary]','3.2.3','library','infra/gateway/Dockerfile','NOASSERTION'),
 ('python','3.12-slim','platform','infra/gateway/Dockerfile','NOASSERTION'),
 ('apache/kafka','3.9.1','container','docker-compose.yml','NOASSERTION'),
 ('timescale/timescaledb','2.18.2-pg16','container','docker-compose.yml','NOASSERTION'),
 ('setuptools','>=68','build-tool','research-python/pyproject.toml','NOASSERTION'),
 ('actions/checkout','v4','ci',' .github/workflows/verify.yml'.strip(),'NOASSERTION'),
 ('actions/setup-python','v5','ci','.github/workflows/verify.yml','NOASSERTION'),
]
# Detect source manifest drift instead of silently emitting stale inventory.
assert 'kafka-python==2.0.2' in (ROOT/'infra/gateway/Dockerfile').read_text()
assert 'psycopg[binary]==3.2.3' in (ROOT/'infra/gateway/Dockerfile').read_text()
compose=(ROOT/'docker-compose.yml').read_text()
for image in ('apache/kafka:3.9.1','timescale/timescaledb:2.18.2-pg16'): assert image in compose
components=[];packages=[]
for i,(name,version,kind,origin,license_) in enumerate(items):
    key='oc2-'+str(i)
    comp={'type':'application' if kind=='application' else 'library' if kind in ('library','build-tool','ci') else 'container' if kind=='container' else 'framework','bom-ref':key,'name':name,'version':version,'properties':[{'name':'oc2:inventory_basis','value':'declared-source'},{'name':'oc2:source_path','value':origin},{'name':'oc2:resolution_status','value':'not-fully-resolved'}]}
    if license_!='NOASSERTION':comp['licenses']=[{'license':{'id':license_}}]
    components.append(comp)
    packages.append({'SPDXID':'SPDXRef-Package-'+str(i),'name':name,'versionInfo':version,'downloadLocation':'NOASSERTION','filesAnalyzed':False,'licenseConcluded':'NOASSERTION','licenseDeclared':license_,'copyrightText':'NOASSERTION','externalRefs':[]})
files=[]
for path in sorted(ROOT.rglob('*')):
    if not path.is_file() or any(p in {'.git','.build','__pycache__'} for p in path.parts):continue
    rel=path.relative_to(ROOT).as_posix()
    if rel.startswith('compliance/') or rel=='SHA256SUMS.txt':continue
    files.append({'path':rel,'sha256':digest(path)})
components[0]['properties'].append({'name':'oc2:source_files_hashed','value':str(len(files))})
metadata={'timestamp':'2026-10-24T00:00:00Z','tools':[{'vendor':'OC2','name':'source-inventory-generator','version':VERSION}],'component':components[0]}
cdx={'bomFormat':'CycloneDX','specVersion':'1.5','serialNumber':'urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'oc2-sbom-'+VERSION)),'version':1,'metadata':metadata,'components':components,'dependencies':[{'ref':'oc2-0','dependsOn':[c['bom-ref'] for c in components[1:]]}]}
(OUT/'sbom.cyclonedx.json').write_text(json.dumps(cdx,indent=2)+'\n')
spdx={'spdxVersion':'SPDX-2.3','dataLicense':'CC0-1.0','SPDXID':'SPDXRef-DOCUMENT','name':'OC2-OCCULUS-'+VERSION,'documentNamespace':'https://example.invalid/oc2/spdx/'+VERSION,'creationInfo':{'created':'2026-10-24T00:00:00Z','creators':['Tool: OC2-source-inventory-generator-'+VERSION]},'packages':packages,'relationships':[{'spdxElementId':'SPDXRef-DOCUMENT','relatedSpdxElement':'SPDXRef-Package-0','relationshipType':'DESCRIBES'}]+[{'spdxElementId':'SPDXRef-Package-0','relatedSpdxElement':'SPDXRef-Package-'+str(i),'relationshipType':'DEPENDS_ON'} for i in range(1,len(packages))]}
(OUT/'sbom.spdx.json').write_text(json.dumps(spdx,indent=2)+'\n')
crypto=[
 ('Ed25519','signature','Sources/OCCULUSCore/Evidence.swift','CryptoKit Curve25519.Signing; ephemeral signer key; iOS'),
 ('Ed25519','signature','scripts/verify_evidence.py','Python cryptography public-key verification'),
 ('SHA-256','hash','Sources/OCCULUSCore/Evidence.swift','CryptoKit SHA256 payload integrity'),
 ('SHA-256','hash','scripts/verify_evidence.py','hashlib SHA-256 payload integrity'),
 ('SHA-256','hash','SHA256SUMS.txt','repository source integrity digests'),
 ('TLS','protocol','services/gateway.py','NOT CONFIGURED: HTTP gateway currently uses plaintext'),
 ('SASL/TLS','protocol','docker-compose.yml','NOT CONFIGURED: Kafka PLAINTEXT listener'),
 ('TLS','protocol','docker-compose.yml','NOT CONFIGURED: DB internal transport not configured'),
 ('Bearer API token','authentication','services/gateway.py','shared token; NOT cryptographic signature; no TLS'),
]
assets=[]
for i,(alg,typ,source,notes) in enumerate(crypto):
    assert (ROOT/source).exists(),source
    assets.append({'type':'cryptographic-asset','bom-ref':'crypto-'+str(i),'name':alg+' / '+source,'cryptoProperties':{'assetType':'algorithm' if typ in ('signature','hash') else 'protocol','algorithmProperties':{'primitive':'signature' if typ=='signature' else 'hash' if typ=='hash' else 'unknown','parameterSetIdentifier':alg} } if typ in ('signature','hash') else {'assetType':'protocol'},'properties':[{'name':'oc2:source_path','value':source},{'name':'oc2:usage','value':notes},{'name':'oc2:status','value':'observed' if typ in ('signature','hash') else 'unprotected-or-not-cryptographic'}]})
cbom={'bomFormat':'CycloneDX','specVersion':'1.6','serialNumber':'urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'oc2-cbom-'+VERSION)),'version':1,'metadata':{'timestamp':'2026-10-24T00:00:00Z','component':{'type':'application','name':'OC2-OCCULUS','version':VERSION}},'components':assets}
(OUT/'cbom.cyclonedx.json').write_text(json.dumps(cbom,indent=2)+'\n')
(OUT/'source-hashes.json').write_text(json.dumps({'version':VERSION,'scope':'repository source files excluding generated compliance files and SHA256SUMS','files':files},indent=2)+'\n')
print('SBOM',len(components),'declared components; CBOM',len(assets),'crypto observations; hashed',len(files),'files')
