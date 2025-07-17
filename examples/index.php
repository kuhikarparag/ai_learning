<?php
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
    // Deliberate error: should return true if no divisors found
    return false; // <-- This is incorrect!
}

// Example usage:
var_dump(isPrime(7)); // Should be true, but returns false
?>