import numpy as np

from View import View

class Receiver(object):

    def __init__(self, space, origin, cube_dimension, material):
        self._origin = np.copy(origin)
        self._space = space
        self._views = []
        self._material = material

        polygons = space.cube(self._origin, cube_dimension, material, True)
        for p in polygons:
            self._views.append(View(self._origin, p))

    def search(self, show_projections=False):
        sources = []

        for it in range(0,5):
            resolved = []

            while len(self._views) > 0:
                v = self._views.pop(0)
                resolved += v.search(self._space.polygons)

            while len(resolved) > 0:
                v = resolved.pop(0)

                material = v.region.target.material

                if material.is_source():
                    if show_projections:
                        v.show_history(self._space)
                    sources.append(v.copy())

                if material.is_refractive():
                    tv, rv = v.refract_view()
                    #self._space.cube(rv.region.origin, 0.1, self._material, True)
                    self._views.append(tv) # through-view
                    self._views.append(rv) # refracted view
                elif material.is_reflective():
                    self._views.append(v.reflect_view())

            print("Sources total: " + str(len(sources)))
