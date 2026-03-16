import { useState } from "react";
import Header from "../components/Header.jsx";
import UploadCard from "../components/UploadCard.jsx";

export default function Landing(){

const[file,setFile]=useState(null);

const[fileObj,setFileObj]=useState(null);
const[result,setResult]=useState(null);
const[loading,setLoading]=useState(false);

async function analyze(fileObj){

if(!fileObj){

alert("Upload image first");

return;

}

setLoading(true);

const formData=new FormData();

formData.append("file",fileObj);

try{

const response=await fetch(

"https://slaycam-backend.vercel.app/api/analyze",

{

method:"POST",

body:formData

}

);

const data=await response.json();

setResult({

score:data.score,

tips:data.analysis.suggestions

});

}catch(e){

console.log(e);

alert("Analysis failed");

}

setLoading(false);

}

return(

<div className="page">

<Header/>

<section className="hero">

<div className="heroContent">

<h1>

Camera ready <br/>

<span>before you record</span>

</h1>

<p>

AI camera coach for creators.
Fix lighting, angle and setup instantly.

</p>

<div className="ctaRow">

<button className="primary">

Try SlayCam

</button>

<button className="secondary">

See Demo

</button>

</div>

</div>

</section>

<section className="demoCard">

<h2>

Check your Slay Score

</h2>
<UploadCard
file={file}
setFile={setFile}
setFileObj={setFileObj}
analyze={()=>analyze(fileObj)}
/>

{loading &&(

<div className="loading">

AI analyzing your setup…

</div>

)}

{result &&(

<div className="result">

<div className="scoreCircle">

{result.score}

</div>

<div className="tips">

{result.tips.map((t,i)=>(

<div key={i} className="tip">

✓ {t}

</div>

))}

</div>

</div>

)}

</section>

<section className="finalCTA">

<h2>

Start creating better content today

</h2>

<button className="primary">

Join Waitlist

</button>

</section>

<footer className="footer">

© SlayCam.ai

</footer>

</div>

);

}