export default function ResultCard({result}){

return(

<div className="resultCard">

<h2>

Your Slay Score

</h2>

<div className="score">

{result.score}

</div>

<h3>

Slay Tips

</h3>

<ul>

{result.tips.map((tip,index)=>(

<li key={index}>

{tip}

</li>

))}

</ul>

</div>

);

}