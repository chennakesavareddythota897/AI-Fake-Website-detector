// export async function scanWebsite(url){
//     return new Promise((resolve)=>{
//         setTimeout(()=>{
//             const safe = Math.random() > 0.5;

//             resolve({
//                 status:safe ? "🟢 SAFE" : "🔴 PHISHING",
//                 riskScore:safe ? 10 : 90,
//                 reasons:safe
//                 ? ["HTTPS Enabled","Trusted Domain"]
//                 :  ["Suspicious Domain", "No HTTPS",
//                     "Blacklisted Website"]
//                   });   
//         },2000);
//     });
// }

export async function scanWebsite() {
    const response = await
    fetch("http://127.0.0.1:8000/scan");
    const data = await response.json();
    return data;

}