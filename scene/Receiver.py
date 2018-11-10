import numpy as np

from View import View

class Receiver(object):

    def __init__(self, space, origin, cube_dimension, material):
        self._origin = np.copy(origin)
        self._space = space
        self._views = []

        polygons = space.cube(self._origin, cube_dimension, material, True)
        for p in polygons:
            self._views.append(View(self._origin, p))

    def search(self, show_projections=False):
        sources = []

        for it in range(1,3):
            resolved = []

            while len(self._views) > 0:
                v = self._views.pop(0)
                resolved += v.search(self._space.polygons)

            while len(resolved) > 0:
                v = resolved.pop(0)

                if show_projections:
                    poly = v.region.window
                    poly.ill_only = poly.plane.basis_k * it # make the polygon illustrative only and offset it
                    self._space.add_poly(poly)

                material = v.region.target.material

                if material.is_source():
                    print("Source view added")
                    sources.append(v.copy())

                if material.is_reflective():
                    self._views.append(v.reflect_view())
                elif material.is_refractive():
                    self._views.append(v.refract_view())
