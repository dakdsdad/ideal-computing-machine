import{_ as v,d as y,u as C,i as B,c as x,b as e,w as o,F as $,m as r,e as a,o as D,f as S,g as l}from"./index.d18d7cbb.js";import{a as k}from"./index.15c82977.js";/* empty css              */const N=y({setup(){const t=C(),u=B({name:""});return{handleChange:n=>{console.log(`selected ${n}`)},formState:u,onFinish:n=>{k.post("/api/repo/add",n).then(s=>{s.data.code===0?(r.success("\u6DFB\u52A0\u6210\u529F"),t.push("/repo")):r.error(s.data.msg)}).catch(s=>{r.error(s)})},onFinishFailed:n=>{console.log("Failed:",n)}}}}),R=l("\u65B0\u589E\u7269\u54C1"),V={style:{"text-align":"center"}},w=l("\u6DFB\u52A0");function A(t,u,_,d,m,n){const s=a("a-breadcrumb-item"),c=a("a-breadcrumb"),p=a("a-input"),i=a("a-form-item"),f=a("a-button"),F=a("a-form"),h=a("a-layout-content"),b=a("a-layout");return D(),x($,null,[e(c,{style:{margin:"16px 0"}},{default:o(()=>[e(s,null,{default:o(()=>[R]),_:1})]),_:1}),e(b,null,{default:o(()=>[e(h,{style:{padding:"50px 50px",background:"rgb(255, 255, 255)"}},{default:o(()=>[e(F,{model:t.formState,name:"basic",autocomplete:"off",onFinish:t.onFinish,onFinishFailed:t.onFinishFailed},{default:o(()=>[e(i,{label:"\u7269\u54C1\u540D\u79F0",name:"name",rules:[{required:!0,message:"\u8BF7\u8F93\u5165\u7269\u54C1\u540D\u79F0"}]},{default:o(()=>[e(p,{value:t.formState.name,"onUpdate:value":u[0]||(u[0]=g=>t.formState.name=g)},null,8,["value"])]),_:1}),e(i,null,{default:o(()=>[S("div",V,[e(f,{type:"primary","html-type":"submit"},{default:o(()=>[w]),_:1})])]),_:1})]),_:1},8,["model","onFinish","onFinishFailed"])]),_:1})]),_:1})],64)}var U=v(N,[["render",A]]);export{U as default};