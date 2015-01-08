#ifndef PYTHONIC_NUMPY_MAX_HPP
#define PYTHONIC_NUMPY_MAX_HPP

#include "pythonic/utils/proxy.hpp"
#include "pythonic/numpy/reduce.hpp"

namespace pythonic {

    namespace numpy {
        template<class E>
          auto max(E&& e) -> decltype(reduce<operator_::proxy::imax>(std::forward<E>(e))) {
            return reduce<operator_::proxy::imax>(std::forward<E>(e));
          }
        template<class E, class Opt>
          auto max(E&& e, Opt&& opt) -> decltype(reduce<operator_::proxy::imax>(std::forward<E>(e), std::forward<Opt>(opt))) {
            return reduce<operator_::proxy::imax>(std::forward<E>(e), std::forward<Opt>(opt));
          }

        PROXY(pythonic::numpy, max);

    }

}

#endif

