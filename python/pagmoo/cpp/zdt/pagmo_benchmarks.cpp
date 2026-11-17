// pagmo_benchmarks.cpp
// DEAP-compatible pybind11 bridge to pagmo2 benchmark problems (ZDT, DTLZ)

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pagmo/problem.hpp>
#include <pagmo/problems/dtlz.hpp>
#include <pagmo/problems/zdt.hpp>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace py = pybind11;

class PagmoBenchmark {
public:
    PagmoBenchmark(const std::string& suite,
                   unsigned int prob_id,
                   unsigned int dim = 30,
                   unsigned int nobj = 3) {
        if (suite == "zdt") {
            // ZDT1..ZDT6: prob_id in [1, 6], dim is decision vector length
            prob_ = pagmo::problem{pagmo::zdt{prob_id, dim}};
        } else if (suite == "dtlz") {
            // DTLZ1..DTLZ7: prob_id in [1, 7], dim >= nobj
            prob_ = pagmo::problem{pagmo::dtlz{prob_id, dim, nobj}};
        } else {
            throw std::invalid_argument("Unsupported suite: use 'zdt' or 'dtlz'");
        }
    }

    // DEAP-compatible evaluate function: accepts list/Individual, returns tuple of floats
    py::tuple evaluate(const std::vector<double>& x) const {
        pagmo::vector_double f = prob_.fitness(x);
        py::tuple res(f.size());
        for (std::size_t i = 0; i < f.size(); ++i) {
            res[i] = f[i];
        }
        return res;
    }

    std::pair<std::vector<double>, std::vector<double>> get_bounds() const {
        return prob_.get_bounds();
    }

    std::size_t get_nx() const { return prob_.get_nx(); }
    std::size_t get_nobj() const { return prob_.get_nobj(); }
    std::string get_name() const { return prob_.get_name(); }

private:
    pagmo::problem prob_;
};

PYBIND11_MODULE(pagmo_benchmarks, m) {
    m.doc() = "DEAP-compatible pybind11 bridge to pagmo2 benchmark problems (ZDT, DTLZ)";

    py::class_<PagmoBenchmark>(m, "PagmoBenchmark")
        .def(py::init<const std::string&, unsigned int, unsigned int, unsigned int>(),
             py::arg("suite"),
             py::arg("prob_id"),
             py::arg("dim") = 30,
             py::arg("nobj") = 3)
        .def("evaluate", &PagmoBenchmark::evaluate,
             "Evaluate decision vector x and return objective tuple")
        .def("get_bounds", &PagmoBenchmark::get_bounds,
             "Return (lower_bounds, upper_bounds)")
        .def("get_nx", &PagmoBenchmark::get_nx)
        .def("get_nobj", &PagmoBenchmark::get_nobj)
        .def("get_name", &PagmoBenchmark::get_name);
}
