"""Exercise the actual release Lua against a small Unreal API test double."""
from pathlib import Path
from lupa.lua54 import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'Voyage/Binaries/Win64/ue4ss/Mods/CaretakerCompass/Scripts/main.lua'
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute(r'''
nextAddress=0; objects={}; widgets={}; controllerScans=0; compassScans=0; playing=false
function object(fields)
 nextAddress=nextAddress+1
 local o=fields or {};o.address=nextAddress;o.valid=true
 function o:IsValid() return self.valid end
 function o:GetAddress() return self.address end
 return o
end
function stringValue(s) return {ToString=function()return s end} end
world=object();pawn=object({boat=false})
function pawn:IsA(_)return self.boat end
pc=object({Pawn=pawn,bShowMouseCursor=false,bCinematicMode=false,dialog=false,intro=false,overlay=false})
function pc:IsLocalPlayerController()return true end
function pc:GetWorld()return world end
function pc:HasActiveDialog()return self.dialog end
function pc:HasIntroWidgetFocus()return self.intro end
function pc:IsPlayerHudWidgetVisible(t)assert(t==2);return self.overlay end
hud=object({bShowHUD=true});function pc:GetHUD()return hud end
instance=object();function instance:IsPlaying()return playing end
class=object();boatClass=object();library=object()
function library:Create(context,cls,owner)
 assert(context==pc and owner==pc and cls==class)
 local w=object({viewport=false,CompassImage=object()})
 function w:SetCustomPawn(p)self.pawn=p end
 function w:SetVisibility(v)self.visibility=v end
 function w:AddToViewport(z)self.viewport=true;self.z=z end
 function w:IsInViewport()return self.viewport end
 function w:RemoveFromParent()self.viewport=false end
 function w:SetAnchorsInViewport(a)self.anchors=a end
 function w:SetAlignmentInViewport(a)self.alignment=a end
 function w:SetPositionInViewport(p,remove)self.position=p;self.anchors=nil;assert(remove==false)end
 function w.CompassImage:SetDesiredSizeOverride(size)self.size=size end
 function w:SetDesiredSizeInViewport(size)self.size=size end
 function w:SetRenderOpacity(v)self.opacity=v end
 widgets[#widgets+1]=w;return w
end
function StaticFindObject(path)
 if path:find('WidgetBlueprintLibrary',1,true)then return library end
 if path:find('VoyageBoatPawn',1,true)then return boatClass end
 return class
end
function FindFirstOf(c)assert(c=='VoyageGameInstance');return instance end
function FindAllOf(c)
 if c=='VoyagePlayerController'then controllerScans=controllerScans+1;return {pc} end
 if c=='WBP_CompassHUD_C'then compassScans=compassScans+1;return {} end
 error('Unexpected object scan '..c)
end
function LoopInGameThreadWithDelay(ms,fn)assert(ms==250);tick=fn end
function activeCount()local n=0;for _,w in ipairs(widgets)do if w.viewport then n=n+1 end end;return n end
''')
lua.globals().SCRIPT = str(SCRIPT).replace('\\', '/')
lua.execute("mod=dofile(SCRIPT)")
cases = {
    'no HUD in menu': 'tick();assert(activeCount()==0)',
    'one centered HUD on world entry': 'playing=true;tick();assert(activeCount()==1 and mod.widget.visibility==3 and mod.widget.anchors.Minimum.X==0.5)',
    'steady state uses cached handles': 'for i=1,240 do tick()end;assert(activeCount()==1 and mod.created==1 and controllerScans==1 and compassScans==1)',
    'boat class suppresses duplicate': 'pawn.boat=true;tick();assert(mod.widget.visibility==1);pawn.boat=false;tick();assert(mod.widget.visibility==3)',
    'menus and HUD toggle recover': '''
for _,k in ipairs({'bShowMouseCursor','dialog','intro','overlay'})do
 pc[k]=true;tick();assert(mod.widget.visibility==1);pc[k]=false;tick();assert(mod.widget.visibility==3)
end
hud.bShowHUD=false;tick();assert(mod.widget.visibility==1);hud.bShowHUD=true;tick();assert(mod.widget.visibility==3)
''',
    'pawn change rebinds without duplicate': 'local old=pawn;pawn=object({boat=false,IsA=old.IsA});pc.Pawn=pawn;tick();assert(mod.widget.pawn==pawn and mod.created==1)',
    'external viewport removal recovers': 'mod.widget:RemoveFromParent();tick();assert(activeCount()==1 and mod.created==2)',
    'world change replaces old HUD': 'world=object();tick();assert(activeCount()==1 and mod.created==3)',
    'return to menu removes HUD': 'playing=false;tick();assert(activeCount()==0)',
    'reload save creates one HUD': 'playing=true;tick();assert(activeCount()==1 and mod.created==4)',
    'script reload stops old updater': 'old=mod;oldTick=tick;mod=dofile(SCRIPT);assert(activeCount()==0);tick();oldTick();assert(activeCount()==1 and old.stopped)',
    'shutdown removes HUD': 'mod.stop();tick();assert(activeCount()==0)',
}
for name, code in cases.items():
    lua.execute(code)
    print('PASS', name)
print(f'{len(cases)} lifecycle scenarios passed')
