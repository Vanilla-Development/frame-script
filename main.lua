-- I used grok just to actually check everything and its putting all these warnings marked as [SPOOF], if you don't care about them then leave it but if you care about them for some reason, then remove the warnings.

getgenv().Config = {
	vic   = 954058593,        -- UserId to fetch avatar/username
	help  = "dmalibrarys",              -- Player being spoofed (DONT LEAVE EMPTY FOR LOCALPLAYER, PASTE YOUR OWN USERNAME OR ITS GLOBAL CHANGES.)
	level = 128,             -- PlayerLevel override
	clan  = "WeOAK",           -- ClanTag override
	kit   = "Lassy"         -- Kit override
}

local Players     = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local CoreGui     = game:GetService("CoreGui")
local RunService  = game:GetService("RunService")
local LocalPlayer = Players.LocalPlayer

local KIT_URL = "https://raw.githubusercontent.com/Vanilla-Development/frame-script/refs/heads/main/kit-table.json"
local KitTable = {}

local function safeCall(fn) local ok,res=pcall(fn) return ok,res end
local function log(msg) print("[SPOOF]", msg) end

local function loadKitTable()
	log("Downloading kit table from GitHub")
	local ok, body = safeCall(function() return game:HttpGet(KIT_URL) end)
	if ok and body then
		local success, decoded = pcall(function() return HttpService:JSONDecode(body) end)
		if success and type(decoded) == "table" then
			log("Kit table downloaded and loaded successfully")
			-- Convert keys to lowercase for case-insensitive matching
			local normalizedTable = {}
			for kitName, assetId in pairs(decoded) do
				normalizedTable[string.lower(kitName)] = assetId
			end
			return normalizedTable
		else
			warn("[SPOOF] Downloaded JSON invalid or empty")
		end
	else
		warn("[SPOOF] Failed to download kit table")
	end
	return {}
end

KitTable = loadKitTable()

local function getTargetPlayer()
	if getgenv().Config.help == "" then
		return LocalPlayer
	end
	return Players:FindFirstChild(getgenv().Config.help)
end

local TargetPlayer = getTargetPlayer()
if not TargetPlayer then
	warn("Target player not found.")
	return
end

local fetchedUsername, fetchedDisplayName
local decodedData = {}
do
	local success, result = pcall(function()
		local url = "https://users.roblox.com/v1/users/" .. tostring(getgenv().Config.vic)
		return HttpService:JSONDecode(game:HttpGet(url))
	end)

	if success and result then
		fetchedUsername    = result.name
		fetchedDisplayName = result.displayName or result.name
		decodedData.name   = result.name
		decodedData.id     = getgenv().Config.vic
		log("Fetched vic userdata: "..fetchedUsername)
	else
		warn("Failed to fetch user info.")
		fetchedUsername    = TargetPlayer.Name
		fetchedDisplayName = TargetPlayer.DisplayName
		decodedData.name   = TargetPlayer.Name
		decodedData.id     = TargetPlayer.UserId
	end
end

local function getEscapeImage() return "rbxthumb://type=Avatar&id="..getgenv().Config.vic.."&w=100&h=100" end
local function getHostPanelImage() return "rbxthumb://type=AvatarHeadShot&id="..getgenv().Config.vic.."&w=48&h=48" end
local function getTabListImage() return "rbxthumb://type=AvatarHeadShot&id="..getgenv().Config.vic.."&w=352&h=352" end
local function getKillFeedImage() return "rbxthumb://type=AvatarHeadShot&id="..getgenv().Config.vic.."&w=150&h=150" end

local function lockImage(imageLabel, desired)
	if imageLabel and imageLabel.Image ~= desired then 
		imageLabel.Image = desired 
	end
	if imageLabel then
		local connection
		connection = imageLabel:GetPropertyChangedSignal("Image"):Connect(function()
			if imageLabel.Image ~= desired then 
				imageLabel.Image = desired 
			end
		end)
		return connection
	end
end

pcall(function()
	TargetPlayer.Name = fetchedUsername
	TargetPlayer.DisplayName = fetchedDisplayName
end)

pcall(function()
	TargetPlayer:SetAttribute("PlayerLevel", getgenv().Config.level)
	if TargetPlayer:GetAttribute("ClanTag") == nil then
		TargetPlayer:SetAttribute("ClanTag","")
	end
	TargetPlayer:SetAttribute("ClanTag", getgenv().Config.clan)
end)

TargetPlayer.AttributeChanged:Connect(function(attr)
	if attr=="PlayerLevel" then 
		TargetPlayer:SetAttribute("PlayerLevel",getgenv().Config.level)
	elseif attr=="ClanTag" then 
		TargetPlayer:SetAttribute("ClanTag",getgenv().Config.clan) 
	end
end)

-- Persistent nametag spoof - survives zoom/first-person
local function spoofNametag()
	local head = TargetPlayer.Character:FindFirstChild("Head")
	if not head then return end
	
	local nametag = head:FindFirstChild("Nametag", true)
	if not nametag then return end
	
	local label = nametag:FindFirstChild("DisplayName", true)
	if not label or not label:IsA("TextLabel") then return end
	
	label.Text = fetchedDisplayName
	
	local conn = label:GetPropertyChangedSignal("Text"):Connect(function()
		if label.Text ~= fetchedDisplayName then
			label.Text = fetchedDisplayName
		end
	end)
	
	label.AncestryChanged:Connect(function()
		task.wait(0.1)
		spoofNametag()
	end)
end

RunService.Heartbeat:Connect(spoofNametag)

local function onCharacterAdded(char)
	task.wait(0.5)
	spoofNametag()
end

if TargetPlayer.Character then onCharacterAdded(TargetPlayer.Character) end
TargetPlayer.CharacterAdded:Connect(onCharacterAdded)

if TargetPlayer.Character then spoofNametag(TargetPlayer.Character) end
TargetPlayer.CharacterAdded:Connect(spoofNametag)

local function hookEscapeMenu()
	local ok, playersFrame = pcall(function()
		return CoreGui.RobloxGui.SettingsClippingShield.SettingsShield.MenuContainer.Page.PageViewClipper.PageView.PageViewInnerFrame.Players
	end)
	if not ok or not playersFrame then return end
	for _, child in ipairs(playersFrame:GetChildren()) do
		if child.Name == "PlayerLabel"..fetchedUsername then
			local icon = child:FindFirstChild("Icon",true)
			if icon and icon:IsA("ImageLabel") then
				lockImage(icon,getEscapeImage())
			end
		end
	end
end

task.spawn(function()
	while true do
		hookEscapeMenu()
		task.wait(1)
	end
end)

task.spawn(function()
	while true do
		local gui = LocalPlayer:FindFirstChild("PlayerGui")
		if not gui then 
			task.wait(0.5)
			continue 
		end
		
		local hostPanel = gui:FindFirstChild("CustomMatchHostPanel")
		if not hostPanel then 
			task.wait(0.5)
			continue 
		end
		
		-- Try to find the scrolling frame dynamically (handles nested/numbered paths)
		local autoCanvas = nil
		for _, desc in ipairs(hostPanel:GetDescendants()) do
			if desc:IsA("ScrollingFrame") and desc.Name == "AutoCanvasScrollingFrame" then
				autoCanvas = desc
				break
			end
		end
		
		if not autoCanvas then 
			task.wait(0.5)
			continue 
		end
		
		-- Scan every possible HostPanelPlayerRow
		for _, row in ipairs(autoCanvas:GetChildren()) do
			if row.Name == "HostPanelPlayerRow" or row.Name:find("PlayerRow") then
				local isTargetRow = false
				
				-- Look for TextLabel with @username
				for _, child in ipairs(row:GetDescendants()) do
					if child:IsA("TextLabel") and child.Text:match("^@") then  -- starts with @
						if child.Text == "@" .. fetchedUsername or child.Text:find(fetchedUsername) then
							isTargetRow = true
							break
						end
					end
				end
				
				if isTargetRow then
					-- Spoof only the avatar images in this row
					for _, img in ipairs(row:GetDescendants()) do
						if img:IsA("ImageLabel") and typeof(img.Image) == "string" and 
						   (img.Image:find("AvatarHeadShot") or img.Image:find("rbxthumb://type=AvatarHeadShot")) then
							lockImage(img, getHostPanelImage())
						end
					end
				end
			end
		end
		
		task.wait(0.5)  -- Balanced polling
	end
end)

local kitSpoofConnections = {}

local function spoofKitImage()
	local kitName = getgenv().Config.kit
	local kitNameLower = string.lower(kitName)
	local kitAsset = KitTable[kitNameLower]
	
	if not kitAsset then 
		warn("[SPOOF] Kit '"..kitName.."' not found in table. Available kits:")
		for k, _ in pairs(KitTable) do
			print("  - " .. k)
		end
		return 
	end

	local gui = LocalPlayer:FindFirstChild("PlayerGui")
	if not gui then return end
	local tabGui = gui:FindFirstChild("TabListScreenGui")
	if not tabGui then return end

	-- Clear old connections
	for _, conn in pairs(kitSpoofConnections) do
		conn:Disconnect()
	end
	kitSpoofConnections = {}

	-- Search recursively, ignoring numbered instances
	for _, label in ipairs(tabGui:GetDescendants()) do
		if label:IsA("TextLabel") and (label.Text == fetchedDisplayName or label.Text:find(fetchedDisplayName)) then  -- Match spoofed name
			local rowContainer = label:FindFirstAncestor("PlayerRowContainer")  -- Stable ancestor
			if rowContainer then
				-- Spoof kit image (broad name match)
				for _, img in ipairs(rowContainer:GetDescendants()) do
					if img:IsA("ImageLabel") and (img.Name:find("PlayerKitImage") or img.Name:find("KitImage") or img.Name:find("Kit")) then
						local conn = lockImage(img, kitAsset)
						if conn then
							table.insert(kitSpoofConnections, conn)
						end
					end
				end
				
				-- Spoof tab list avatar (broad name match)
				for _, child in ipairs(rowContainer:GetDescendants()) do
					if child:IsA("ImageLabel") and (child.Name:find("PlayerRender") or child.Name:find("PlayerInfo") or child.Name:find("Render")) then
						lockImage(child, getTabListImage())
					end
				end
			end
		end
	end
	
	log("Kit & tab avatar spoof applied for: " .. fetchedDisplayName)
end

-- Monitor for new UI elements (handles dynamic adds)
RunService.DescendantAdded:Connect(function(descendant)
	if descendant:IsA("ImageLabel") and (descendant.Name:find("KitImage") or descendant.Name:find("PlayerRender")) then
		task.wait(0.1) -- Wait for UI init
		spoofKitImage()
	end
end)

-- Run periodically to catch UI reloads
task.spawn(function()
	while true do
		spoofKitImage()
		task.wait(1)  -- Faster for reactivity
	end
end)

local function spoofKillfeed()
	local gui = LocalPlayer:FindFirstChild("PlayerGui")
	if not gui then return end
	local kf = gui:FindFirstChild("KillFeedGui")
	if not kf then return end
	local container = kf:FindFirstChild("KillFeedContainer")
	if not container then return end

	for _, cardWrapper in ipairs(container:GetChildren()) do
		for _, card in ipairs(cardWrapper:GetChildren()) do
			local inner = card:FindFirstChild("KillFeedCardInner")
			if inner then
				for _, img in ipairs(inner:GetDescendants()) do
					if img:IsA("ImageLabel") and typeof(img.Image)=="string" then
						if img.Image:find("id="..tostring(LocalPlayer.UserId)) or img.Image:find("id="..tostring(TargetPlayer.UserId)) then
							lockImage(img, getKillFeedImage())
						end
					end
				end
			end
		end
	end
end

LocalPlayer.PlayerGui.ChildAdded:Connect(function(child)
	if child.Name == "KillFeedGui" then
		child.DescendantAdded:Connect(spoofKillfeed)
		child.ChildRemoved:Connect(spoofKillfeed)
	end
end)

RunService.Heartbeat:Connect(spoofKillfeed)


-- FIXED CHARACTER SPOOF WITH INVENTORY PROTECTION
local characterSpoofed = false

local function spoofCharacter(plr, vicId)
	if not plr.Character or not plr.Character:FindFirstChild("Humanoid") then 
		return false
	end

	local char = plr.Character
	local humanoid = char.Humanoid
	
	-- Don't respoof if already done (to prevent item loss on respawn)
	if characterSpoofed and char:GetAttribute("Spoofed") == vicId then
		return true
	end

	-- Store ALL tools in Backpack (safe, Roblox handles re-equip)
	local backpack = plr:FindFirstChild("Backpack")
	if not backpack then return false end
	
	local savedItems = {}
	for _, child in pairs(char:GetChildren()) do
		if child:IsA("Tool") or child:IsA("Model") or child:IsA("BasePart") then
			-- Only save non-rig items
			if not (child:IsA("BasePart") and child.Name == "HumanoidRootPart") and
			   not (child:IsA("BasePart") and (child.Name == "Head" or child.Name == "Torso" or child.Name == "Left Arm" or 
											child.Name == "Right Arm" or child.Name == "Left Leg" or child.Name == "Right Leg")) then
				table.insert(savedItems, child)
				child.Parent = backpack -- Safe relocation
			end
		end
	end

	-- Fetch and apply appearance
	local success, appearance = pcall(function()
		return Players:GetCharacterAppearanceAsync(vicId)
	end)
	
	if not success or not appearance then
		warn("Appearance fetch failed, restoring items")
		for _, item in pairs(savedItems) do
			item.Parent = char
		end
		return false
	end

	-- Remove only cosmetics, not character structure
	for _, item in pairs(char:GetChildren()) do
		if item:IsA("Accessory") or item:IsA("Shirt") or item:IsA("Pants") or 
		   item:IsA("ShirtGraphic") or item:IsA("BodyColors") or item:IsA("Decal") then
			item:Destroy()
		end
	end

	-- Apply new cosmetics
	for _, item in pairs(appearance:GetChildren()) do
		local itemClone = item:Clone()
		if item:IsA("Shirt") or item:IsA("Pants") or item:IsA("ShirtGraphic") or item:IsA("BodyColors") then
			itemClone.Parent = char
		elseif item:IsA("Accessory") then
			humanoid:AddAccessory(itemClone)
		end
	end

	-- Face handling
	local head = char:FindFirstChild("Head")
	if head then
		local face = head:FindFirstChild("face")
		if face then face:Destroy() end
		local vicFace = appearance:FindFirstChild("face")
		if vicFace then
			vicFace:Clone().Parent = head
		end
	end

	-- Restore saved items (Roblox re-equips Tools)
	for _, item in pairs(savedItems) do
		item.Parent = char
	end

	-- Mark as spoofed to prevent reapplication
	char:SetAttribute("Spoofed", vicId)
	characterSpoofed = true
	
	-- Rebuild rig if needed
	pcall(function()
		humanoid:BuildRigFromAttachments()
	end)
	
	log("Character spoof applied successfully with inventory protection")
	return true
end

local function applyCharacterSpoof()
	if not getgenv().Config.vic then return end
	
	-- Wait a bit for character to fully load
	task.wait(0.5)
	
	local success = spoofCharacter(TargetPlayer, getgenv().Config.vic)
	if not success then
		-- Retry once after a delay
		task.wait(1)
		spoofCharacter(TargetPlayer, getgenv().Config.vic)
	end
end

-- Handle character changes
TargetPlayer.CharacterAdded:Connect(function(char)
	task.wait(1) -- Wait for character to fully load
	characterSpoofed = false
	applyCharacterSpoof()
end)

-- Also apply when script starts
if TargetPlayer.Character then
	task.spawn(function()
		task.wait(1)
		applyCharacterSpoof()
	end)
end

-- Monitor for respawns
TargetPlayer.CharacterRemoving:Connect(function()
	characterSpoofed = false
end)

print("done loading, if you need the kit table then goto github.com/vanilla-development/frame-script/kit-table.json")
print("you can also get the avaliable kits at the same repo as the kit table, just check avaliable.txt since you have to type them EXACTLY and case sensitive")
