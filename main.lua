-- I used gpt just to actually check everything and its putting all these warnings marked as [SPOOF], if you don't care about them then leave it but if you care about them for some reason, then remove the warnings.

getgenv().Config = {
	vic   = 5591992,        -- UserId to fetch avatar/username
	help  = "",              -- Player being spoofed (leave empty for LocalPlayer)
	level = 98,             -- PlayerLevel override
	clan  = "gg",           -- ClanTag override
	kit   = "Caitlyn"         -- Kit override
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

local function applyNametag(character)
	local head = character:WaitForChild("Head",5)
	if not head then return end
	local tag = head:FindFirstChild("Nametag",true)
	if not tag then return end
	local label = tag:FindFirstChild("DisplayName",true)
	if label and label:IsA("TextLabel") then
		label.Text = fetchedDisplayName
		label:GetPropertyChangedSignal("Text"):Connect(function()
			if label.Text ~= fetchedDisplayName then label.Text = fetchedDisplayName end
		end)
	end
end

if TargetPlayer.Character then applyNametag(TargetPlayer.Character) end
TargetPlayer.CharacterAdded:Connect(applyNametag)

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
		for _, inst in ipairs(LocalPlayer:GetDescendants()) do
			if inst.Name=="HostPanelPlayerRow" then
				for _, child in ipairs(inst:GetDescendants()) do
					if child:IsA("ImageLabel") and typeof(child.Image)=="string" and child.Image:find("rbxthumb://type=AvatarHeadShot") then
						lockImage(child,getHostPanelImage())
					end
				end
			end
		end
		task.wait(0.25)
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

  
	for _, conn in pairs(kitSpoofConnections) do
		conn:Disconnect()
	end
	kitSpoofConnections = {}
  
	for _, pd in ipairs(tabGui:GetDescendants()) do
		if pd:IsA("ImageLabel") and (pd.Name=="PlayerKitImage" or pd.Name=="KitImage") then
			local conn = lockImage(pd, kitAsset)
			if conn then
				table.insert(kitSpoofConnections, conn)
			end
		end
	end
	
	for _, frame in ipairs(tabGui:GetDescendants()) do
		if frame:IsA("Frame") then
			for _, child in ipairs(frame:GetChildren()) do
				if child:IsA("ImageLabel") and (child.Name=="PlayerKitImage" or child.Name=="KitImage" or child.Name=="Kit") then
					local conn = lockImage(child, kitAsset)
					if conn then
						table.insert(kitSpoofConnections, conn)
					end
				end
			end
		end
	end
	
	log("Kit spoof applied: " .. kitName .. " -> " .. kitAsset)
end


RunService.DescendantAdded:Connect(function(descendant)
	if descendant:IsA("ImageLabel") and (descendant.Name=="PlayerKitImage" or descendant.Name=="KitImage" or descendant.Name=="Kit") then
		task.wait(0.1) -- Wait for UI to initialize
		spoofKitImage()
	end
end)


task.spawn(function()
	while true do
		spoofKitImage()
		task.wait(2)
	end
end)

task.spawn(function()
	while true do
		local gui = LocalPlayer:FindFirstChild("PlayerGui")
		if gui then
			local tabGui = gui:FindFirstChild("TabListScreenGui")
			if tabGui then
				for _, inst in ipairs(tabGui:GetDescendants()) do
					if inst:IsA("Frame") and inst.Name=="PlayerDropdown" then
						for _, child in ipairs(inst:GetDescendants()) do
							if child:IsA("ImageLabel") and child.Name=="PlayerRender" then
								lockImage(child,getTabListImage())
							end
						end
					end
				end
			end
		end
		task.wait(0.25)
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


local characterSpoofed = false

local function spoofCharacter(plr, vicId)
	if not plr.Character or not plr.Character:FindFirstChild("Humanoid") then 
		return false
	end

	local char = plr.Character
	local humanoid = char.Humanoid
	

	if characterSpoofed and char:GetAttribute("Spoofed") == vicId then
		return true
	end


	local savedItems = {}
	local itemParents = {}
	
	for _, child in pairs(char:GetChildren()) do
		if child:IsA("Tool") or child:IsA("Model") or child:IsA("BasePart") then
			-- Only save items that aren't part of the character's base structure
			if not (child:IsA("BasePart") and child.Name == "HumanoidRootPart") and
			   not (child:IsA("BasePart") and (child.Name == "Head" or child.Name == "Torso" or child.Name == "Left Arm" or 
												child.Name == "Right Arm" or child.Name == "Left Leg" or child.Name == "Right Leg")) then
				table.insert(savedItems, child)
				itemParents[child] = child.Parent
				child.Parent = nil
			end
		end
	end


	local success, appearance = pcall(function()
		return Players:GetCharacterAppearanceAsync(vicId)
	end)
	
	if not success or not appearance then
		warn("Appearance fetch failed, restoring items")
		for _, item in pairs(savedItems) do
			if item and item.Parent == nil then
				item.Parent = char
			end
		end
		return false
	end

	for _, item in pairs(char:GetChildren()) do
		if item:IsA("Accessory") or item:IsA("Shirt") or item:IsA("Pants") or 
		   item:IsA("ShirtGraphic") or item:IsA("BodyColors") or item:IsA("Decal") then
			item:Destroy()
		end
	end

	for _, item in pairs(appearance:GetChildren()) do
		local itemClone = item:Clone()
		if item:IsA("Shirt") or item:IsA("Pants") or item:IsA("ShirtGraphic") or item:IsA("BodyColors") then
			itemClone.Parent = char
		elseif item:IsA("Accessory") then
			humanoid:AddAccessory(itemClone)
		end
	end

	local head = char:FindFirstChild("Head")
	if head then
		local face = head:FindFirstChild("face")
		if face then face:Destroy() end
		local vicFace = appearance:FindFirstChild("face")
		if vicFace then
			vicFace:Clone().Parent = head
		end
	end

	for _, item in pairs(savedItems) do
		if item and item.Parent == nil then
			item.Parent = char
		end
	end

	char:SetAttribute("Spoofed", vicId)
	characterSpoofed = true
	
	pcall(function()
		humanoid:BuildRigFromAttachments()
	end)
	
	log("Character spoof applied successfully with inventory protection")
	return true
end

local function applyCharacterSpoof()
	if not getgenv().Config.vic then return end
	
	task.wait(0.5)
	
	local success = spoofCharacter(TargetPlayer, getgenv().Config.vic)
	if not success then
		task.wait(1)
		spoofCharacter(TargetPlayer, getgenv().Config.vic)
	end
end

TargetPlayer.CharacterAdded:Connect(function(char)
	task.wait(1)
	characterSpoofed = false
	applyCharacterSpoof()
end)

if TargetPlayer.Character then
	task.spawn(function()
		task.wait(1)
		applyCharacterSpoof()
	end)
end

TargetPlayer.CharacterRemoving:Connect(function()
	characterSpoofed = false
end)

print("done loading, if you need the kit table then goto github.com/vanilla-development/frame-script/kit-table.json")
print("you can also get the avaliable kits at the same repo as the kit table, just check avaliable.txt since you have to type them EXACTLY and case sensitive")
