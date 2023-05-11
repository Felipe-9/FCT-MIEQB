export function bin(n,k) {
    // Checking if n and k are integer
    if(Number.isNaN(n) || Number.isNaN(k)) return NaN;
    if(k < 0 || k > n)         return 0;
    if(k === 0 || k === n)     return 1;
    if(k === 1 || k === n - 1) return n;

    return Math.round(
        Array.from({length:k}, (_,i) => (n-i)/(i+1))
        .reduce((prod,value) => prod * value)
    );
};

// const IPEIO = await import("./IPEIO.mjs")