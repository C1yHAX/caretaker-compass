-- Caretaker Compass 1.0.0: independent HUD lifecycle using the current game's compass.
-- The game calculates direction/degree text. No copied cooked third-party assets,
-- frame hooks, key bindings, save changes, or native memory patches are required.
local folder = debug.getinfo(1, 'S').source:sub(2):match('^(.*[/\\])')
local config = dofile(folder .. 'config.lua')
local M = {version = '1.0.0', created = 0, stopped = false}
local TAG = 'CaretakerCompass.Runtime'
local CLASS = '/Game/UI/Game/World/WBP_CompassHUD.WBP_CompassHUD_C'
local state = {retry = 0, visibility = nil, cleaned = false}
local function log(s) print('[CaretakerCompass] ' .. s .. '\n') end
local function valid(o)
    if o == nil then return false end
    local ok, result = pcall(function() return o:IsValid() end)
    return ok and result == true
end
local function address(o) return valid(o) and o:GetAddress() or nil end
local function bounded(v, default, lo, hi)
    v = tonumber(v)
    if not v or v ~= v then return default end
    return math.max(lo, math.min(hi, v))
end
local width = bounded(config.Width, 820, 240, 1400)
local top = bounded(config.Top, 12, 0, 500)
local height = bounded(config.StripHeight, 32, 16, 96)
local opacity = bounded(config.Opacity, 0.95, 0.1, 1)

function M.remove()
    if valid(state.widget) then pcall(function() state.widget:RemoveFromParent() end) end
    state.widget, state.owner, state.world, state.pawn = nil, nil, nil, nil
    state.visibility = nil
    M.widget = nil
end
function M.stop() M.stopped = true; M.remove() end
local previous = rawget(_G, 'CaretakerCompass')
if previous and previous.stop then previous.stop() end
_G.CaretakerCompass = M

local function show(visible)
    local value = visible and 3 or 1 -- HitTestInvisible / Collapsed
    if state.visibility ~= value and valid(state.widget) then
        state.widget:SetVisibility(value)
        state.visibility = value
    end
end

local function create(pc, pawn, world)
    if not valid(state.class) then
        state.class = StaticFindObject(CLASS)
        if not valid(state.class) then
            -- Only called from the game-thread scheduler, never from a UFunction hook.
            LoadAsset(CLASS)
            state.class = StaticFindObject(CLASS)
        end
    end
    assert(valid(state.class), 'Current game compass class unavailable')
    if not state.cleaned then
        -- A one-time scan removes only our own orphaned widgets after script reload.
        for _, widget in ipairs(FindAllOf('WBP_CompassHUD_C') or {}) do
            if valid(widget) and widget.WidgetPersistentKey:ToString() == TAG then
                widget:RemoveFromParent()
            end
        end
        state.cleaned = true
    end
    local library = StaticFindObject('/Script/UMG.Default__WidgetBlueprintLibrary')
    local widget = library:Create(pc, state.class, pc)
    assert(valid(widget), 'Compass widget creation failed')
    state.widget, M.widget = widget, widget
    widget.WidgetPersistentKey = TAG
    widget.bUseControllerDirection = true
    widget.bUseDynamicIndicatorIcon = false
    widget:SetCustomPawn(pawn)
    widget:SetVisibility(3)
    -- The viewport owns the widget; Lua references alone do not prevent Unreal GC.
    widget:AddToViewport(-10)
    widget:SetAlignmentInViewport({X = 0.5, Y = 0})
    widget:SetPositionInViewport({X = 0, Y = top}, false)
    widget.CompassImage:SetDesiredSizeOverride({X = width, Y = height})
    widget:SetDesiredSizeInViewport({X = width, Y = height + 64})
    -- SetPositionInViewport resets anchors to (0,0) in this engine build.
    widget:SetAnchorsInViewport({Minimum = {X = 0.5, Y = 0}, Maximum = {X = 0.5, Y = 0}})
    widget:SetRenderOpacity(opacity)
    state.owner, state.world, state.pawn = address(pc), address(world), address(pawn)
    state.visibility = 3
    M.created = M.created + 1
    log('HUD ready; native direction, no input bindings (instance ' .. M.created .. ')')
end

function M.update()
    if M.stopped then return end
    if config.Enabled == false then M.remove(); return end
    if not valid(state.instance) then state.instance = FindFirstOf('VoyageGameInstance') end
    if not valid(state.instance) or not state.instance:IsPlaying() then
        M.remove(); state.pc = nil; return
    end
    if not valid(state.pc) then
        for _, pc in ipairs(FindAllOf('VoyagePlayerController') or {}) do
            if valid(pc) and pc:IsLocalPlayerController() then state.pc = pc; break end
        end
    end
    local pc = state.pc
    if not valid(pc) then M.remove(); return end
    local pawn, world = pc.Pawn, pc:GetWorld()
    if not valid(pawn) or not valid(world) then M.remove(); return end
    if state.owner ~= address(pc) or state.world ~= address(world) then M.remove() end
    if valid(state.widget) and not state.widget:IsInViewport() then M.remove() end
    if not valid(state.widget) then
        if state.retry > 0 then state.retry = state.retry - 1; return end
        state.retry = 20 -- at most one failed creation attempt every five seconds
        create(pc, pawn, world)
        state.retry = 0
    elseif state.pawn ~= address(pawn) then
        state.widget:SetCustomPawn(pawn)
        state.pawn = address(pawn)
    end
    local visible = true
    if config.HideWhileSteering ~= false then
        if not valid(state.boatClass) then state.boatClass = StaticFindObject('/Script/Voyage.VoyageBoatPawn') end
        if valid(state.boatClass) and pawn:IsA(state.boatClass) then visible = false end
    end
    if config.HideInMenus ~= false then
        if pc.bShowMouseCursor == true or pc:HasActiveDialog() or pc:HasIntroWidgetFocus()
            or pc:IsPlayerHudWidgetVisible(2) then visible = false end
    end
    local hud = pc:GetHUD()
    -- Cinematic mode itself is not a reflected property in this game build.
    -- Follow the real HUD visibility instead of reading an unresolved UE4SS member.
    if valid(hud) and hud.bShowHUD == false then visible = false end
    show(visible)
end

if not LoopInGameThreadWithDelay then
    log('Requires a UE4SS build with LoopInGameThreadWithDelay; compass inactive')
    return M
end
LoopInGameThreadWithDelay(250, function()
    if M.stopped then return true end
    local ok, err = pcall(M.update)
    if not ok then
        M.remove()
        state.retry = 20
        if state.lastError ~= tostring(err) then log('Update failed: ' .. tostring(err)); state.lastError = tostring(err) end
    end
end)
log('1.0.0 loaded; waiting for the local player')
return M
