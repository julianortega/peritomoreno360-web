# Carta de la marca. «{M}» se sustituye por el nombre de la marca (config en build.py).
# Fuente: grupos y opciones de Flight Director (carta_grupos / carta_grupo_opciones, leído 2026-10-07),
# gramos del «Protocolo de cantidades» V2 junio-26 (tortilla: 1 unidad, estimada en 75 g; verduras: 120 g en el vegetal, 70 g en el normal) y composición por 100 g de tablas de referencia.
import json
C={
 'tortilla':[310,8.0,3.0,50,2.5,3.0,8.5,1.4],'cero':[0]*8,
 'pollo':[165,5.0,1.4,1.0,0.5,0,29,0.9],'crispy':[260,13,2.0,17,0.8,1.0,18,1.2],
 'cochinita':[200,11,4.0,3.0,2.0,0.5,22,1.1],'res':[190,10,4.0,3.0,1.5,0.8,21,1.0],'verduras':[45,2.5,0.4,4.5,3.5,2.0,1.3,0.4],
 'arroz':[140,2.0,0.4,28,0.2,0.5,2.7,0.4],'integral':[125,1.5,0.3,25,0.3,1.8,2.7,0.3],'frijoles':[115,0.5,0.1,15,0.3,8.7,8.9,0.4],
 'pico':[25,0.2,0,4.5,3.0,1.3,1.0,0.4],'maiz':[86,1.2,0.2,17,4.5,2.4,3.2,0.3],'cebolla':[40,0.1,0,8.5,6.0,1.2,1.0,1.0],
 'guaca':[160,14.5,2.1,4.5,0.7,6.7,2.0,0.6],'rallado':[360,28,18,1.0,0.5,0,25,1.6],'fundido':[210,15,9.0,8.0,3.0,0,9.0,1.8],
 'verde':[30,0.5,0.1,5.0,3.0,1.5,1.0,1.0],'roja':[35,0.5,0,6.0,4.0,2.0,1.3,1.3],'inferno':[45,1.2,0.2,7.0,4.5,2.5,1.5,1.4],
 'agria':[190,19,12,3.0,3.0,0,2.5,0.1],'chipotle':[300,30,2.5,6.0,3.0,0.5,1.0,1.4],'chips':[490,23,2.5,63,1.0,5.0,7.0,1.0],
 'lechuga':[15,0.2,0.03,1.7,1.2,1.3,1.4,0.03],
}
def O(i,n,parts,price=0,al=None,default=False,unit=None): return dict(id=i,name=n,parts=parts,price=price,al=al or [],default=default,unit=unit)
# key, título, mínimo, máximo, ayuda, opciones, solo_tienda
GROUPS=[
 ('formato','Formato',1,1,'Elige uno',[O('burrito','Burrito',[('tortilla',75)],al=['Gluten'],default=True,unit='1 tortilla'),O('bowl','Bowl',[('cero',0)])],False),
 ('proteina','Proteína',1,1,'Elige una',[O('crispy','Pollo crispy',[('crispy',130)],al=['Gluten','Huevo']),O('plancha','Pollo plancha',[('pollo',130)]),O('res','Res estofada',[('res',130)],1.00),O('cochinita','Cochinita pibil',[('cochinita',130)]),O('vegetal','Vegetal (verduras al wok)',[('verduras',120)])],False),
 ('arroz','Arroz',1,1,'Elige uno',[O('blanco','Arroz blanco',[('arroz',90)],default=True),O('integral','Arroz integral',[('integral',90)]),O('sinarroz','Sin arroz',[('cero',0)])],False),
 ('ingredientes','Ingredientes',0,10,'Los que quieras',[O('frijoles','Frijoles',[('frijoles',80)]),O('fundido','Queso fundido',[('fundido',30)],0.50,['Leche']),O('verduras','Verduras al wok',[('verduras',70)]),O('pico','Pico de gallo',[('pico',50)]),O('maiz','Maíz mix',[('maiz',40)]),O('cebolla','Cebolla encurtida',[('cebolla',20)],al=['Sulfitos']),O('guaca','Guacamole casero',[('guaca',85)],2.25),O('agria','Crema agria',[('agria',30)],0.50,['Leche']),O('chipotle','Crema chipotle',[('chipotle',30)],0.50,['Huevo','Mostaza']),O('rallado','Queso rallado',[('rallado',30)],0.25,['Leche']),O('lechuga','Lechuga',[('lechuga',80)])],False),
 ('salsas','Salsas',0,3,'Hasta 3',[O('verde','Verde · pica 2/10',[('verde',30)]),O('roja','Roja · pica 5/10',[('roja',30)]),O('inferno','Inferno · pica 9/10',[('inferno',30)],0.25)],False),
 ('extras','Extras',0,4,'Con suplemento',[O('xplancha','Extra pollo plancha',[('pollo',130)],2.50),O('xcrispy','Extra pollo crispy',[('crispy',130)],2.50,['Gluten','Huevo']),O('xcochinita','Extra cochinita',[('cochinita',130)],2.50),O('xres','Extra res',[('res',130)],2.95)],False),
 ('picante','Picante',0,1,'Opcional',[O('p0','Sin picante',[('cero',0)]),O('p1','Suave',[('cero',0)]),O('p2','Medio',[('cero',0)]),O('p3','{M}',[('cero',0)])],True),
]
PICAR=('picar','Para picar',0,3,'Los que quieras',[O('nachos','Nachos',[('chips',250),('frijoles',140),('fundido',240),('pico',140),('guaca',120),('agria',80)],al=['Leche']),O('totoqueso','Totopos con queso',[('chips',150),('fundido',200)],al=['Leche'])],False)
PRESETS=[('El Salvaje',{'formato':['burrito'],'proteina':['crispy'],'arroz':['blanco'],'ingredientes':['frijoles','maiz','chipotle','lechuga'],'salsas':[]}),
 ('La Indómita',{'formato':['burrito'],'proteina':['plancha'],'arroz':['blanco'],'ingredientes':['frijoles','pico','lechuga'],'salsas':['verde','roja']}),
 ('El Jabalí',{'formato':['burrito'],'proteina':['cochinita'],'arroz':['blanco'],'ingredientes':['frijoles','cebolla','agria','lechuga'],'salsas':[]}),
 ('Inferno',{'formato':['burrito'],'proteina':['res'],'arroz':['blanco'],'ingredientes':['frijoles','guaca','pico'],'salsas':['inferno']})]
BASE_PRICE=8.95  # «Burrito {M} (individual)», precio sala en Flight Director

def tot(parts): return [round(sum(C[k][j]*g/100 for k,g in parts),2) for j in range(8)]
def groups_json(groups):
    return [{'key':k,'title':t,'min':mn,'max':mx,'hint':h,'items':[{'id':o['id'],'name':o['name'],'g':sum(g for _,g in o['parts']),'v':tot(o['parts']),'al':o['al'],'price':o['price'],'def':o['default'],**({'u':o['unit']} if o['unit'] else {})} for o in opts]} for k,t,mn,mx,h,opts,_ in groups]
def calc_data():
    gs=[g for g in GROUPS if not g[6]]+[PICAR]
    return json.dumps({'groups':groups_json(gs),'presets':[{'name':n,'sel':s} for n,s in PRESETS]},ensure_ascii=False)
def shop_data():
    return {'groups':groups_json(GROUPS),'presets':[{'name':n,'sel':s} for n,s in PRESETS],'base':BASE_PRICE}

# Productos de carta (precio sala de Flight Director). (id, nombre, descripción, precio, foto en assets/img o None)
PRODUCTS=[
 ('bestiales','Los {M}es','Nuestras recetas de la casa, en burrito o en bowl.',[
   ('salvaje','El Salvaje','Pollo crunchy, arroz, frijoles, maíz, crema chipotle y lechuga.',15.95,'p-salvaje'),
   ('indomita','La Indómita','Pollo a la plancha, arroz, frijoles, pico de gallo, salsas verde y roja y lechuga.',15.95,'p-indomita'),
   ('jabali','El Jabalí','Cochinita pibil, arroz, frijoles, cebolla encurtida, crema agria y lechuga.',15.95,'p-jabali'),
   ('inferno','Inferno','Res guisada, arroz, frijoles, guacamole, pico de gallo y salsa de picante extremo.',16.95,'p-inferno')]),
 ('packs','Packs ahorro','Burritos a tu medida para compartir (o no).',[
   ('duo','Dúo {M}','2 burritos a tu medida.',15.95,'p-duo'),
   ('trio','Trío {M}','3 burritos a tu medida.',23.50,'p-trio'),
   ('pack','{M} Pack','4 burritos a tu medida.',29.95,'p-pack')]),
 ('tacos','Tacos y quesadillas','Tortilla de maíz, al momento.',[
   ('tlegendario','Taco Legendario','',2.95,'p-tlegendario'),
   ('tsatan','Taco Satán','',2.95,'p-tsatan'),
   ('tsupremo','Taco Supremo','',2.95,'p-tsupremo'),
   ('tdama','Taco La Dama','',2.95,'p-tdama'),
   ('qqueso','Quesadilla solo queso','',9.95,None),
   ('qpollo','Quesadilla de pollo','',9.95,None),
   ('qres','Quesadilla de res','',9.95,None)]),
 ('compartir','Para compartir','Para el centro de la mesa.',[
   ('nachos','Nachos','Totopos, frijoles, queso fundido, pico de gallo, guacamole y crema agria.',12.00,'p-nachos'),
   ('totoguaca','Totopos con guaca','',4.95,'p-totoguaca'),
   ('totoqueso','Totopos con queso','',4.95,'p-totoqueso'),
   ('guacaxl','Guacamole XL','',5.95,None),
   ('croquetas','Croquetas de jalapeño','',6.95,None)]),
 ('bebidas','Bebidas','',[
   ('ipa','{M} Session IPA sin gluten','33 cl',2.95,None),
   ('cocacola','Coca-Cola','330 ml',2.00,None),('cocazero','Coca-Cola Zero','330 ml',2.00,None),
   ('fantal','Fanta Limón','330 ml',2.00,None),('fantan','Fanta Naranja','330 ml',2.00,None),('sprite','Sprite','330 ml',2.00,None),
   ('fuze','Fuze Tea','330 ml',2.00,None),('aqn','Aquarius naranja','330 ml',2.00,None),('aql','Aquarius limón','330 ml',2.00,None),
   ('agua','Ocean52 sin gas','33 cl',1.50,None),('aguagas','Ocean52 con gas','33 cl',1.50,None)]),
 ('postres','Postres','',[
   ('lima','Tarta de lima','',4.95,None),('brownie','Brownie','',3.50,None),
   ('cookie3','Cookie triple chocolate','',3.50,None),('cookiebelga','Cookie chip chocolate belga','',2.95,None),
   ('cookiefr','Cookie chocolate blanco y frambuesa','',3.50,None),
   ('kibar','KI-BAR','Coco, manzana, vainilla o cacao.',1.00,None)]),
]
