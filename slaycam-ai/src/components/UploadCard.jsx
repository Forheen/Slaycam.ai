export default function UploadCard({file,setFile,setFileObj,analyze}){

function handleFile(e){

const selected=e.target.files[0];

if(selected){

setFile(URL.createObjectURL(selected));

setFileObj(selected);

}

}

return(

<div className="uploadCard">

<input 
type="file"
onChange={handleFile}
/>

{file &&(

<img
src={file}
className="preview"
/>

)}

<button
onClick={analyze}
className="analyzeBtn"
>

Analyze Setup

</button>

</div>

);

}