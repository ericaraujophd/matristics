"""Generate an arched stained-glass window (Voronoi cells clipped to an arch)
as an inline SVG string, in the Calvin palette. Output: mosaic.svg"""
import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
rng=np.random.default_rng(7)
W,H=400,560; R=W/2
arch=unary_union([box(0,R,W,H), Point(R,R).buffer(R,resolution=64)])
inner=arch.buffer(-14)
pts=rng.uniform([0,0],[W,H],(70,2))
pts=np.vstack([pts,[[-500,-500],[1500,-500],[-500,1500],[1500,1500]]])
vor=Voronoi(pts)
cols=['#D9A93E','#8E2F3F','#EFE6D2','#3E7D6B','#4C7FA8','#C76A6A','#E5C77E','#6E1C2E']
w=[.22,.14,.18,.1,.1,.08,.12,.06]
cells=[]; centers=[]
for i,reg in enumerate(vor.point_region[:-4]):
    r=vor.regions[reg]
    if -1 in r or not r: continue
    poly=Polygon([vor.vertices[k] for k in r]).intersection(inner)
    if poly.is_empty or poly.area<40: continue
    poly=poly.buffer(-2.5)
    if poly.is_empty or poly.geom_type!='Polygon': continue
    c=rng.choice(cols,p=np.array(w)/sum(w))
    d='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in poly.exterior.coords)+'Z'
    cells.append(f'<path d="{d}" fill="{c}"/>'); centers.append(poly.centroid)
# a few network edges between nearby cell centres (echoing the network motif)
edges=[]
cs=[(c.x,c.y) for c in centers]
for i,(x,y) in enumerate(cs):
    ds=sorted(((x-a)**2+(y-b)**2,j) for j,(a,b) in enumerate(cs) if j!=i)[:2]
    for _,j in ds:
        if i<j: edges.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{cs[j][0]:.0f}" y2="{cs[j][1]:.0f}"/>')
dots=''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.5"/>' for x,y in cs)
ad='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in arch.exterior.coords)+'Z'
svg=(f'<svg viewBox="-6 -6 412 572" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
     f'<path d="{ad}" fill="#2B1218" stroke="#C49A2C" stroke-width="8"/>'
     + ''.join(cells) +
     f'<g stroke="#FFF8E8" stroke-opacity=".55" stroke-width="1.6">{"".join(edges)}</g>'
     f'<g fill="#FFF8E8" stroke="#2B1218" stroke-width="1.5">{dots}</g></svg>')
open('mosaic.svg','w').write(svg); print(len(cells),'cells',len(svg),'bytes')
