import os
import numpy as np
import pybullet as p
import pybullet_data
from abc import ABC, abstractmethod

class BaseScene(ABC):
    def __init__(self, world, config, rng, test=False, validate=False):
        self._world = world
        self._rng = rng
        self._model_path = pybullet_data.getDataPath()
        self._validate = validate
        self._test = test
        self.extent = config.get('extent', 0.1)
        self.max_objects = config.get('max_objects', 6)
        self.min_objects = config.get('min_objects', 1)
        object_samplers = {'wooden_blocks': self._sample_wooden_blocks,
                           'random_urdfs': self._sample_random_objects,
                           'objs': self._sample_custom_objects,
                           'objsnew': self._sample_sdf_objects,
                           'scored_obj': self._sample_scored_objects,
                           'egad_eval': self._sample_egad_objects,
                           'ycb': self._sample_ycb_objects}
        self._object_sampler = object_samplers[config['scene']['data_set']]
        print("dataset", config['scene']['data_set'])

    def _sample_wooden_blocks(self, n_objects):
        self._model_path = "models/"
        object_names = ['circular_segment', 'cube',
                        'cuboid0', 'cuboid1', 'cylinder', 'triangle']
        selection = self._rng.choice(object_names, size=n_objects)
        paths = [os.path.join(self._model_path, 'wooden_blocks',
                              name + '.urdf') for name in selection]
        return paths, 1.
    
    def _sample_custom_objects(self, n_objects):
        self._model_path = "models/"
        object_names = ['one', 'two',
                        'three', 'four', 'five']
        selection = self._rng.choice(object_names, size=n_objects)
        paths = [os.path.join(self._model_path, 'objs',
                              name + '.urdf') for name in selection]
        return paths, 1.

    def _sample_sdf_objects(self, n_objects):
        self._model_path = "models/"
        object_names = ['two']
        selection = self._rng.choice(object_names, size=n_objects)
        paths = [os.path.join(self._model_path, 'objsnew',
                              name + '.sdf') for name in selection]
        return paths, 0.5
    
    def _sample_scored_objects(self, n_objects):
        self._model_path = "models/"
        object_names = ['mesh_1591920030', 'mesh_1591920050', 'mesh_1591920064', 'mesh_1591920123', 'mesh_1591920340',
                        'mesh_1591920803', 'mesh_1591921352', 'mesh_1591921446', 'mesh_1591921760', 'mesh_1591922017',
                        'mesh_1591922262', 'mesh_1591922411', 'mesh_1591922502', 'mesh_1591922941', 'mesh_1591923156',
                        'mesh_1591923279', 'mesh_1591923293', 'mesh_1591923765', 'mesh_1591924029']
        selection = self._rng.choice(object_names, size=n_objects)
        paths = [os.path.join(self._model_path, 'scored_obj',
                              name + '.sdf') for name in selection]
        return paths, 0.45
    
    def _sample_egad_objects(self, n_objects):
        self._model_path = "models/"
        object_names = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B0', 'B1', 'B2',
                        'B3', 'B4', 'B5', 'B6', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5']
        selection = self._rng.choice(object_names, size=n_objects)
        paths = [os.path.join(self._model_path, 'egad_eval',
                              name + '.sdf') for name in selection]
        return paths, 0.0007

    def _sample_ycb_objects(self, n_objects):
        self._model_path = "models/"
        object_names = ['y10', 'y11', 'y12', 'y13', 'y14', 'y15', 'y16', 'y17']
        selection = self._rng.choice(object_names, size=n_objects)
        paths = [os.path.join(self._model_path, 'ycb',
                              name + '.sdf') for name in selection]
        return paths, 0.65

    def _sample_random_objects(self, n_objects):
        if self._validate:
            self.object_range = np.arange(700, 850)
        elif self._test:
            self.object_range = np.arange(850, 1000)
        else: 
            self.object_range = 700
        # object_range = 900 if not self._test else np.arange(900, 1000)
        selection = self._rng.choice(self.object_range, size=n_objects)
        paths = [os.path.join(self._model_path, 'random_urdfs',
                            '{0:03d}/{0:03d}.urdf'.format(i)) for i in selection]
        return paths, 1.

    @abstractmethod
    def reset(self):
        raise NotImplementedError
