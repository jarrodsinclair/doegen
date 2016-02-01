import numpy as np
from openmdao.api import IndepVarComp, Group, Problem
from openmdao.core.component import Component
from openmdao.drivers.fullfactorial_driver import FullFactorialDriver
from openmdao.drivers.latinhypercube_driver import LatinHypercubeDriver, \
    OptimizedLatinHypercubeDriver
from openmdao.drivers.uniform_driver import UniformDriver


_METHOD_TO_DRIVER = {
    'FullFactorial': {
        'cls': FullFactorialDriver,
        'req_args': [
            'num_levels'
        ]
    },
    'Uniform': {
        'cls': UniformDriver,
        'req_args': [
            'num_samples'
        ]
    },
    'LatinHypercube': {
        'cls': LatinHypercubeDriver,
        'req_args': [
            'num_samples'
        ]
    },
    'OptimizedLatinHypercube': {
        'cls': OptimizedLatinHypercubeDriver,
        'req_args': [
            'num_samples'
        ]
    }
}


class _CaptureParams(Component):
    def __init__(self, num_params, doe):
        super(_CaptureParams, self).__init__()
        self._num_params = num_params
        self._doe = doe
        for i in range(num_params):
            self.add_param('v%d' % i, val=0.0)
        self.add_output('vout', val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        d = np.array([], dtype=float)
        for i in range(self._num_params):
            vname = 'v%d' % i
            d = np.append(d, params[vname])
        self._doe.append(d)
        unknowns['vout'] = 0.0


def generate(method, params, **kwargs):
    # map method to openmdao driver
    assert method in _METHOD_TO_DRIVER.keys()
    _driver = _METHOD_TO_DRIVER[method]['cls']

    # cast and check params matix
    if not isinstance(params, np.ndarray):
        params = np.asarray(params, dtype=float)
    assert len(params.shape) == 2
    assert params.shape[1] == 2

    # check for required keyword arguments
    parsed_keys = kwargs.keys()
    for req_arg in _METHOD_TO_DRIVER[method]['req_args']:
        assert req_arg in parsed_keys

    # construct openmdao problem
    num_params = len(params)
    top = Problem()
    top.root = Group()
    top.driver = _driver(**kwargs)
    i = 0
    for vmin, vmax in params:
        pname = 'p%d' % i
        vname = 'v%d' % i
        top.root.add(pname, IndepVarComp(vname, 0.0), promotes=['*'])
        top.driver.add_desvar(vname, lower=float(vmin), upper=float(vmax))
        i += 1
    doe = []
    top.root.add('pout', _CaptureParams(num_params, doe), promotes=['*'])
    top.driver.add_objective('vout')

    # setup, run and terminate the openmdao problem
    top.setup(check=False)
    top.run()
    top.cleanup()
    del top.driver
    del top.root
    del top

    # return as a numpy array
    return np.array(doe)
