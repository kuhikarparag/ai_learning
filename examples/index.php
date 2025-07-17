<?php
function isPrime($n) {
    if ($n <= 1) {
        return false;
    }
    for ($i = 2; $i < $n; $i++) {
        if ($n % $i == 0) {
            return false;
        }
    }
    // Corrected: Return true if no divisors found
    return true;
}

// Example usage:
var_dump(isPrime(7)); // Should now return true
?>