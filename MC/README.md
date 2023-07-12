# Minecraft Part code

## Todo List

1. Skills List

    1. Fireball
    2. Snowball (Cancelled)
    3. TNT
    4. Lightning
    5. Ice Cage
    
2. Camera Setting(Cancelled, using manual camera)

3. Armor Effect Design

## Command Block Code

1. TNT : execute at [username] run summon minecraft:tnt ~ ~ ~ {Fuse:[fusetime]}
2. Fireball : execute at [username] run summon minecraft:fireball ~ ~1 ~ {ExplosivePower:[Power]}
3. Lightning : execute at [username] run summon minecraft:lightning_bolt ~ ~ ~ (Repeat Command Block)
4. Armor:
    /execute at BlueMoon06 run summon minecraft:armor_stand ~-3 ~5 ~10 {NoGravity:1b,NoBasePlate:1b,Invisible:1b,ArmorItems:[{id:"minecraft:diamond_boots",Count:1b}]}
    /execute as @e[type=minecraft:armor_stand,nbt={NoGravity:1b}] at @s facing entity BlueMoon06 feet run tp ^ ^ ^0.8
    /execute as @e[type=minecraft:armor_stand] at @s if entity @e[type=minecraft:player,distance=..0.5] run kill @s
    /setblock 9980 7 9901 minecraft:command_block{Command:"execute at BlueMoon06 run summon minecraft:armor_stand ~-3 ~5 ~10 {NoGravity:1b,NoBasePlate:1b,Invisible:1b,ArmorItems:[{id:\"minecraft:diamond_boots\",Count:1b}]}"} destroy
    /item replace entity BlueMoon06 armor.feet with minecraft:diamond_boots
