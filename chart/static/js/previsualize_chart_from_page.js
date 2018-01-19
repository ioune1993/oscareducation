/* Group 07 */

$(document).ready(function() {
   document.getElementById("validate-yaml").addEventListener("click", function() {setTimeout(clone_chart, 100)});
})

function clone_chart()
{
   console.log("inside")
   let chart = document.getElementById("jxgbox");
   if (chart !== null)
   {
      console.log("inside")
      let previsualization = document.getElementById("previsualized-chart");
      if (previsualization !== null)
      {
         console.log("inside")
         previsualization.innerHTML = chart.innerHTML
      }
   }
}
