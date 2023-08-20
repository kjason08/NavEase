<!DOCTYPE html>
<html>
<head>
  <title>경로 탐색 예제</title>
  <link rel="stylesheet" href="styles.css">
  <script src="path-to-your-js-file.js"></script>
  <script>
    (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})({
      key: "AIzaSyDOgEizKc7rmgXErLwNO9ipv9JCHZ8O4b0",
      // Add other bootstrap parameters as needed, using camel case.
      // Use the 'v' parameter to indicate the version to load (alpha, beta, weekly, etc.)
    });
  </script>
</head>
<body>
  <div>
    <label for="start">출발지:</label>
    <input type="text" id="start" placeholder="출발지 주소">
    <br>
    <label for="end">도착지:</label>
    <input type="text" id="end" placeholder="도착지 주소">
    <br>
    <button onclick="calculateRoute()">경로 탐색</button>
  </div>
  <div id="map" style="height: 400px;"></div>
</body>
</html>
