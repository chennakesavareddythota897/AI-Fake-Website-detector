export async function scanWebsite(url){
    return new Promise((resolve)=>{
        setTimeout(()=>{
            const safe = Math.random() > 0.5;

            resolve({
                status:safe ? "🟢 SAFE" : "🔴 PHISHING",
                riskScore:safe ? 10 : 80,
                reasons:safe
                ? ["HTTPS Enabled","Trusted Domain"]
                :  ["Suspicious Domain", "No HTTPS",
                    "Blacklisted Website"]
                  });   
        },2000);
    });
}