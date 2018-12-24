function log10(x) {
    var y;
    y = Math.log(x) / Math.log(10);   // log_a(x) = log_b(x) / log_b(a)
    return (y);
}

function exp10(x) {
    var y;
    y = Math.exp(x * Math.log(10));   // a^x = b^(x * log_b(a))
    return (y);
}



function convertWTodBm(W) {
    if (isNaN(W) || (W <= 0)) {
        return null;
    }
    var dBW = 10 * log10(W);
    dBm = dBW + 30;
    return dBm;
}
