# -*- coding: utf-8 -*-
"""
This is the unittest of CovModel class.
"""
from __future__ import division, absolute_import, print_function

import numpy as np
import unittest
from gstools import (
    Gaussian,
    Exponential,
    # Spherical,
    SRF,
)


class TestCondition(unittest.TestCase):
    def setUp(self):
        self.cov_models = [
            Gaussian,
            Exponential,
            # Spherical,
        ]
        self.dims = range(1, 4)
        self.data = np.array(
            [
                [0.3, 1.2, 0.5, 0.47],
                [1.9, 0.6, 1.0, 0.56],
                [1.1, 3.2, 1.5, 0.74],
                [3.3, 4.4, 2.0, 1.47],
                [4.7, 3.8, 2.5, 1.74],
            ]
        )
        self.cond_pos = (self.data[:, 0], self.data[:, 1], self.data[:, 2])
        self.cond_val = self.data[:, 3]
        self.mean = np.mean(self.cond_val)
        grid = np.linspace(5, 20, 10)
        self.grid_x = np.concatenate((self.cond_pos[0], grid))
        self.grid_y = np.concatenate((self.cond_pos[1], grid))
        self.grid_z = np.concatenate((self.cond_pos[2], grid))
        self.pos = (self.grid_x, self.grid_y, self.grid_z)

    def test_simple(self):
        print("SIMPLE")
        for Model in self.cov_models:
            print(Model.name)
            for dim in self.dims:
                print("  dim: ", dim)
                model = Model(
                    dim=dim,
                    var=0.5,
                    len_scale=2,
                    anis=[0.1, 1],
                    angles=[0.5, 0, 0],
                )
                srf = SRF(
                    model,
                    self.mean,
                )
                print("    set condition")
                srf.set_condition(
                    self.cond_pos[:dim],
                    self.cond_val,
                    "simple",
                )
                print("    gen unstr")
                field_1 = srf.unstructured(self.pos[:dim])
                print("    gen str")
                field_2 = srf.structured(self.pos[:dim])
                print("    compare")
                for i, val in enumerate(self.cond_val):
                    self.assertAlmostEqual(val, field_1[i], places=2)
                    self.assertAlmostEqual(
                        val, field_2[dim * (i,)], places=2
                    )

    def test_ordinary(self):
        print("ORDINARY")
        for Model in self.cov_models:
            print(Model.name)
            for dim in self.dims:
                print("  dim: ", dim)
                model = Model(
                    dim=dim,
                    var=0.5,
                    len_scale=2,
                    anis=[0.1, 1],
                    angles=[0.5, 0, 0],
                )
                srf = SRF(model)
                print("    set condition")
                srf.set_condition(
                    self.cond_pos[:dim],
                    self.cond_val,
                    "ordinary",
                )
                print("    gen unstr")
                field_1 = srf.unstructured(self.pos[:dim])
                print("    gen str")
                field_2 = srf.structured(self.pos[:dim])
                print("    compare")
                for i, val in enumerate(self.cond_val):
                    self.assertAlmostEqual(val, field_1[i], places=2)
                    self.assertAlmostEqual(
                        val, field_2[dim * (i,)], places=2
                    )


if __name__ == "__main__":
    unittest.main()
