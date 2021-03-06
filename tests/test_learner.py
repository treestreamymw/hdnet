# -*- coding: utf-8 -*-
# This file is part of the hdnet package
# Copyright 2014 the authors, see file AUTHORS.
# Licensed under the GPLv3, see file LICENSE for details

import os
import numpy as np

from hdnet.spikes import Spikes
from hdnet.learner import Learner

from test_tmppath import TestTmpPath


class TestLearner(TestTmpPath):

    def setUp(self):
        super(TestLearner, self).setUp()
        import logging
        logging.disable(level=logging.WARNING)

    def tearDown(self):
        super(TestLearner, self).tearDown()

    def test_basic(self):
        file_contents = np.load(os.path.join(os.path.dirname(__file__), 'test_data/tiny_spikes.npz'))
        spikes = Spikes(file_contents[file_contents.keys()[0]])
        learner = Learner(spikes)
        self.assertEqual(learner._spikes.N, 3)

        learner.learn_from_spikes()
        self.assertTrue(learner._network.J.mean() != 0.)

        learner.learn_from_spikes(spikes)
        self.assertTrue(learner._network.J.mean() != 0.)

        learner.learn_from_spikes(spikes, window_size=3)
        self.assertTrue(learner._network.J.mean() != 0.)
        self.assertTrue(learner._network.J.shape == (9, 9))

        learner._params['hi'] = 'chris'
        learner.save(os.path.join(self.TMP_PATH, 'learner'))
        learner2 = Learner.load(os.path.join(self.TMP_PATH, 'learner'))
        self.assertEqual(learner2.params['hi'], 'chris')
        self.assertEqual(learner2.window_size, 3)
        self.assertTrue(learner2.network.J.mean() != 0.)
        self.assertTrue(learner2.network.J.shape == (9, 9))


# end of source
