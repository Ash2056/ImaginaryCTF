
from base import List
from PIL import Image
from PIL.PyAccess import PyAccess
from PIL.PngImagePlugin import PngImageFile

class Img:
	@staticmethod
	def map(f, *pngs: str, out="out.png"):
		imgs: List[PngImageFile] = list(map(Image.open, pngs))
		pxls: List[PyAccess]		 = [i.load() for i in imgs]
		if len({i.size for i in imgs}) == 1: ValueError("Require all shapes to be identical")
		w, h = imgs[0].size
		for x in range(w):
			for y in range(h):
				pxls[0][x,y] = f(*[p[x,y] for p in pxls])
		imgs[0].save(out)
