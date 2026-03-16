import { useState } from "react";
import Header from "../components/Header.jsx";
import UploadCard from "../components/UploadCard.jsx";

export default function Landing(){

const[file,setFile]=useState(null);
const[result,setResult]=useState(null);
const[loading,setLoading]=useState(false);

function analyze(){

setLoading(true);

setTimeout(()=>{

setResult({

score:86,

tips:[
"Face soft window light",
"Raise camera slightly",
"Use clean background"
]

});

setLoading(false);

},1200);

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
analyze={analyze}
/>

{loading &&(

<div className="loading">

Analyzing setup…

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