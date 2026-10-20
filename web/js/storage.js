(function(){
 const KEY='registroHabitos.v3.accounts', SESSION='registroHabitos.v3.session', LEGACY=['registroHabitos.v2','registroHabitos.v1'];
 let state={user:'Mi espacio',username:'',goal:70,theme:'light',avatar:'🌱',records:{},readNotifications:[]};
 let accounts={}; let active='';
 function safeName(s){return String(s||'').trim().toLocaleLowerCase('es').replace(/\s+/g,' ')}
 function valid(s){return s&&typeof s==='object'&&s.records&&typeof s.records==='object'}
 function load(){
  try{accounts=JSON.parse(localStorage.getItem(KEY)||'{}')||{};active=localStorage.getItem(SESSION)||'';
   if(active&&accounts[active]&&valid(accounts[active].data)){state={...state,...accounts[active].data};return state;}
   active='';state={user:'Mi espacio',username:'',goal:70,theme:'light',avatar:'🌱',records:{},readNotifications:[]};
  }catch(e){accounts={};active='';console.warn('No se pudo leer el registro local.',e)}return state;
 }
 function persistAccounts(){try{localStorage.setItem(KEY,JSON.stringify(accounts));return true}catch(e){alert('No se pudo guardar. Exporta un respaldo y revisa el espacio disponible del navegador.');return false}}
 function save(){if(!active)return false;accounts[active].data=state;return persistAccounts()}
 function register(name,password,requestedUsername){const username=safeName(requestedUsername||name);if(username.length<3)return {ok:false,message:'El usuario debe tener al menos 3 caracteres.'};if(String(password||'').length<4)return {ok:false,message:'La contraseña debe tener al menos 4 caracteres.'};if(accounts[username])return {ok:false,message:'Ese usuario ya existe. Inicia sesión.'};
  const isFirst=Object.keys(accounts).length===0;let initial={user:String(name).trim().slice(0,32),username,goal:70,theme:'light',avatar:'🌱',records:{},readNotifications:[]};
  if(isFirst){for(const key of LEGACY){try{const old=JSON.parse(localStorage.getItem(key)||'null');if(valid(old)){initial={...initial,...old};break}}catch(_){}}}
  state={...initial,user:String(name).trim().slice(0,32),username,goal:Number(initial.goal)||70,theme:initial.theme||'light',avatar:initial.avatar||'🌱',records:initial.records||{},readNotifications:initial.readNotifications||[]};accounts[username]={username,displayName:String(name).trim().slice(0,32),password:String(password),data:state};active=username;if(!persistAccounts())return {ok:false,message:'No se pudo guardar la cuenta.'};localStorage.setItem(SESSION,active);return {ok:true};
 }
 function login(name,password){const username=safeName(name),a=accounts[username];if(!a||a.password!==String(password))return {ok:false,message:'Usuario o contraseña incorrectos.'};active=username;state={...state,...a.data};localStorage.setItem(SESSION,active);return {ok:true}}
 function logout(){save();localStorage.removeItem(SESSION);active='';state={user:'Mi espacio',username:'',goal:70,theme:'light',avatar:'🌱',records:{},readNotifications:[]}}
 function updateProfile(name,avatar){state.user=String(name||'Mi espacio').trim().slice(0,32)||'Mi espacio';state.avatar=avatar||state.avatar||'🌱';if(active&&accounts[active])accounts[active].displayName=state.user;return save()}
 function changePassword(currentPassword,newPassword){if(!active||!accounts[active])return {ok:false,message:'No hay una sesión activa.'};const account=accounts[active];if(account.password!==String(currentPassword||''))return {ok:false,message:'La contraseña actual no coincide.'};if(String(newPassword||'').length<4)return {ok:false,message:'La nueva contraseña debe tener al menos 4 caracteres.'};account.password=String(newPassword);if(!persistAccounts())return {ok:false,message:'No se pudo guardar el cambio. Inténtalo de nuevo.'};return {ok:true,message:'Contraseña actualizada correctamente.'}}
 function day(key){if(!state.records[key])state.records[key]={habitos:{},reflexion:{}};const r=state.records[key];if(!r.habitos)r.habitos={};if(!r.reflexion)r.reflexion={};return r}
 window.HabitStorage={KEY,get state(){return state},get accounts(){return accounts},get active(){return active},load,save,day,register,login,logout,updateProfile,changePassword};
})();
