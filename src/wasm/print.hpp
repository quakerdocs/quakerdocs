/**
 * A helper header for easy printing.
 * @file print.hpp
 * @author Jurriaan van den Berg (jurriaanvdberg@gmail.com)
 * @date 2020-08-17
 *
 * @copyright Copyright (c) 2020
 *
 */

#pragma once

#include <iostream>
#include <iomanip>
#include <sstream>
#include <array>
#include <string>

typedef unsigned int uint;

/** Is true if type type T is convertable to a string. */
template<typename T, typename = int>
struct StringConvertable : std::false_type {};
template<typename T> struct StringConvertable<T,
    decltype (*(std::ostringstream*)(0) << *(T*)(0), 0)> : std::true_type {};

/** A type to convert a type to a string. */
template<typename T, typename = int>
struct Stringifier {
    static std::string get_string( const T& t ) {
        std::ostringstream s;
        s << "<object: " << std::setfill('0') << std::hex << std::uppercase;
        for (unsigned i = 0; i < sizeof (T); ++i) {
            if (i != 0) s << ' ';
            s << std::setw(2) << +reinterpret_cast<const unsigned char*>(&t)[i];
        }
        s << '>';
        return s.str();
    }
};

/* String convertable specialization */
template<typename T>
struct Stringifier<T, std::enable_if_t<StringConvertable<T>::value, int>> {
    static std::string get_string( const T& t ) {
        std::ostringstream s;
        s << t;
        return s.str();
    }
};

/* Iterable type specialization */
template<typename T>
struct Stringifier<T, std::enable_if_t<!StringConvertable<T>::value,
                        decltype (std::begin(std::declval<T>()),
                                  std::end(std::declval<T>()), 0)>> {
    static std::string get_string( const T& iterable ) {
        std::ostringstream s;
        int i = 0;
        s << '{';
        for (const auto& it : iterable) {
            if (i++) s << ", ";
            s << Stringifier<std::remove_const_t<
                std::remove_reference_t<decltype (it)>>>::get_string(it);
        }
        s << '}';
        return s.str();
    }
};

/* std::pair type specialization. */
template<typename T, typename U>
struct Stringifier<std::pair<T,U>> {
    static std::string get_string( const std::pair<T,U>& pair ) {
        std::ostringstream s;
        s << '(' << Stringifier<T>::get_string(pair.first) << ", " <<
                    Stringifier<U>::get_string(pair.second) << ')';
        return s.str();
    }
};


/**
 * Convert just about any type to a string.
 */
template<typename T>
std::string toString( const T& t ) {
    return Stringifier<T>::get_string(t);
}


/**
 * Print about any type, with a seperator inbetween and an ending string.
 */
template<typename ...Args>
void prints( const std::string& seperator, const std::string& end,
             const Args&... args ) {
    std::array<std::string, sizeof...(Args)> strs = {toString(args)...};
    for (uint i = 0; i < sizeof...(Args); ++i) {
        if (i != 0) std::cout << seperator;
        std::cout << strs[i];
    }
    std::cout << end;
}

/**
 * Print just about any type.
 * @param args The values to print.
 */
template<typename ...Args>
void print( const Args&... args ) {
    prints(" ", "\n", args...);
}
