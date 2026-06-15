package com.darkness.db;

import javax.persistence.*;

@Entity
@Table(name = "npcs")
public class NpcDB {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private String name;
    private String description;
    private Integer location;
    private Integer attack;
    private Integer defense;
    private Integer hp;
    private Integer hp_max;
    private Integer mana;
    private Integer mana_max;
    private Integer lvl;
    private Integer money_drop;
    private Integer exp_drop;
    private String aggressive; // "yes" or "no"
    private String faction; // "good", "evil", "neutral", "shopkeeper"
    private String shop_name;
    private String dialog;

    public NpcDB() {}

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Integer getLocation() { return location; }
    public void setLocation(Integer location) { this.location = location; }
    public Integer getAttack() { return attack; }
    public void setAttack(Integer attack) { this.attack = attack; }
    public Integer getDefense() { return defense; }
    public void setDefense(Integer defense) { this.defense = defense; }
    public Integer getHp() { return hp; }
    public void setHp(Integer hp) { this.hp = hp; }
    public Integer getHp_max() { return hp_max; }
    public void setHp_max(Integer hp_max) { this.hp_max = hp_max; }
    public Integer getMana() { return mana; }
    public void setMana(Integer mana) { this.mana = mana; }
    public Integer getMana_max() { return mana_max; }
    public void setMana_max(Integer mana_max) { this.mana_max = mana_max; }
    public Integer getLvl() { return lvl; }
    public void setLvl(Integer lvl) { this.lvl = lvl; }
    public Integer getMoney_drop() { return money_drop; }
    public void setMoney_drop(Integer money_drop) { this.money_drop = money_drop; }
    public Integer getExp_drop() { return exp_drop; }
    public void setExp_drop(Integer exp_drop) { this.exp_drop = exp_drop; }
    public String getAggressive() { return aggressive; }
    public void setAggressive(String aggressive) { this.aggressive = aggressive; }
    public String getFaction() { return faction; }
    public void setFaction(String faction) { this.faction = faction; }
    public String getShop_name() { return shop_name; }
    public void setShop_name(String shop_name) { this.shop_name = shop_name; }
    public String getDialog() { return dialog; }
    public void setDialog(String dialog) { this.dialog = dialog; }
}