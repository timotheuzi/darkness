package com.darkness.db;

import javax.persistence.*;

/**
 * User Entity aligned with MajorMUD core mechanics.
 * Core Attributes: Str, Int, Wil, Agi, Hea, Cha.
 */
@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_user_name", columnList = "name"),
    @Index(name = "idx_user_location", columnList = "location"),
    @Index(name = "idx_user_online", columnList = "online")
})
public class UserDB {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private String name;
    private String password;
    
    // MajorMUD Leveling
    private Integer lvl;
    private Integer exp;
    private Integer exp_max;
    private Integer money;

    // Vitals
    private Integer hp;
    private Integer hp_max;
    private Integer mana;
    private Integer mana_max;

    // MajorMUD Core Attributes
    private Integer str_stat; // Strength
    private Integer int_stat; // Intellectual
    private Integer wil_stat; // Willpower
    private Integer agi_stat; // Agility
    private Integer hea_stat; // Health
    private Integer cha_stat; // Charm

    // Derived Stats
    private Integer attack;
    private Integer defense;

    private String description;
    private Integer location;
    private String race;
    private String game_class;
    
    // Equipment slots (MajorMUD style)
    private Integer weapon_main;
    private Integer weapon_off;
    private Integer armor_head;
    private Integer armor_chest;
    private Integer armor_legs;
    private Integer armor_feet;
    private Integer armor_hands;
    private Integer armor_shield;

    private Integer online; // 1 = Online, 0 = Offline

    public UserDB() {}

    // Getters and Setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public Integer getLvl() { return lvl; }
    public void setLvl(Integer lvl) { this.lvl = lvl; }
    public Integer getExp() { return exp; }
    public void setExp(Integer exp) { this.exp = exp; }
    public Integer getExp_max() { return exp_max; }
    public void setExp_max(Integer exp_max) { this.exp_max = exp_max; }
    public Integer getMoney() { return money; }
    public void setMoney(Integer money) { this.money = money; }
    public Integer getHp() { return hp; }
    public void setHp(Integer hp) { this.hp = hp; }
    public Integer getHp_max() { return hp_max; }
    public void setHp_max(Integer hp_max) { this.hp_max = hp_max; }
    public Integer getMana() { return mana; }
    public void setMana(Integer mana) { this.mana = mana; }
    public Integer getMana_max() { return mana_max; }
    public void setMana_max(Integer mana_max) { this.mana_max = mana_max; }
    public Integer getStr_stat() { return str_stat; }
    public void setStr_stat(Integer str_stat) { this.str_stat = str_stat; }
    public Integer getInt_stat() { return int_stat; }
    public void setInt_stat(Integer int_stat) { this.int_stat = int_stat; }
    public Integer getWil_stat() { return wil_stat; }
    public void setWil_stat(Integer wil_stat) { this.wil_stat = wil_stat; }
    public Integer getAgi_stat() { return agi_stat; }
    public void setAgi_stat(Integer agi_stat) { this.agi_stat = agi_stat; }
    public Integer getHea_stat() { return hea_stat; }
    public void setHea_stat(Integer hea_stat) { this.hea_stat = hea_stat; }
    public Integer getCha_stat() { return cha_stat; }
    public void setCha_stat(Integer cha_stat) { this.cha_stat = cha_stat; }
    public Integer getAttack() { return attack; }
    public void setAttack(Integer attack) { this.attack = attack; }
    public Integer getDefense() { return defense; }
    public void setDefense(Integer defense) { this.defense = defense; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Integer getLocation() { return location; }
    public void setLocation(Integer location) { this.location = location; }
    public String getRace() { return race; }
    public void setRace(String race) { this.race = race; }
    public String getGame_class() { return game_class; }
    public void setGame_class(String game_class) { this.game_class = game_class; }
    public Integer getWeapon_main() { return weapon_main; }
    public void setWeapon_main(Integer weapon_main) { this.weapon_main = weapon_main; }
    public Integer getWeapon_off() { return weapon_off; }
    public void setWeapon_off(Integer weapon_off) { this.weapon_off = weapon_off; }
    public Integer getArmor_head() { return armor_head; }
    public void setArmor_head(Integer armor_head) { this.armor_head = armor_head; }
    public Integer getArmor_chest() { return armor_chest; }
    public void setArmor_chest(Integer armor_chest) { this.armor_chest = armor_chest; }
    public Integer getArmor_legs() { return armor_legs; }
    public void setArmor_legs(Integer armor_legs) { this.armor_legs = armor_legs; }
    public Integer getArmor_feet() { return armor_feet; }
    public void setArmor_feet(Integer armor_feet) { this.armor_feet = armor_feet; }
    public Integer getArmor_hands() { return armor_hands; }
    public void setArmor_hands(Integer armor_hands) { this.armor_hands = armor_hands; }
    public Integer getArmor_shield() { return armor_shield; }
    public void setArmor_shield(Integer armor_shield) { this.armor_shield = armor_shield; }
    public Integer getOnline() { return online; }
    public void setOnline(Integer online) { this.online = online; }
}
