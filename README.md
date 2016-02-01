Doegen
======

A simple Python library that wraps the Design of Experiments (DOE) capability of
[OpenMDAO](http://openmdao.org/) into a single "generate" function call. All DOE
algorithms provided by OpenMDAO are available, including:

 - Full factorial
 - Uniform (random) distribution
 - Latin hypercube
 - Morris-Mitchell optimized Latin hypercube

Basic usage is:

```python
doegen.generate(algorithm_name, parameter_ranges, **kwargs)
```

Where the algorithm name is provided as a string, the parameter ranges are a
defined by a list of min/max values, and algorithm specific keyword arguments
are added at the end.

Example
-------

A more detailed example of each algorithm type follows:

```python
import doegen

# define 3 parameters by their min/max ranges
params = [[0, 1],
          [-5.5, 7.5],
          [300, 600]]

# generate a basic DOE for each algorithm type
print(doegen.generate('FullFactorial', params, num_levels=2))
print(doegen.generate('Uniform', params, num_samples=10))
print(doegen.generate('LatinHypercube', params, num_samples=10))
print(doegen.generate('OptimizedLatinHypercube', params, num_samples=10))

# generate an OLHC with additional algorithm specific arguments
X = doegen.generate('OptimizedLatinHypercube', params, num_samples=30, seed=3,
                    population=50, generations=4)
print('\nDOE points:')
i = 0
for x in X:
    print('Iteration %d: p0=%g, p1=%g, p2=%g' % (i, x[0], x[1], x[2]))
    i += 1
```

Algorithms
----------

The following links provide a reference to the specific arguments of each
algorithm. Note that OpenMDAO adds the word "Driver" to each algorithm.

 - ['FullFactorial'](http://openmdao.readthedocs.org/en/latest/srcdocs/packages/drivers/fullfactorial_driver.html#openmdao.drivers.fullfactorial_driver.FullFactorialDriver)
 - ['Uniform'](http://openmdao.readthedocs.org/en/latest/srcdocs/packages/drivers/uniform_driver.html#openmdao.drivers.uniform_driver.UniformDriver)
 - ['LatinHypercube'](http://openmdao.readthedocs.org/en/latest/srcdocs/packages/drivers/latinhypercube_driver.html#openmdao.drivers.latinhypercube_driver.LatinHypercubeDriver)
 - ['OptimizedLatinHypercube'](http://openmdao.readthedocs.org/en/latest/srcdocs/packages/drivers/latinhypercube_driver.html#openmdao.drivers.latinhypercube_driver.OptimizedLatinHypercubeDriver)
