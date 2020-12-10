package com.darkness.db;

import javax.persistence.*;

//user objects

@Entity
@Table(name = "users")
public class UserDB {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private int id;// test

	private String name;
	private Integer lvl;
	private Integer money;
	private Integer exp;
	private Integer attack;
	private Integer defense;
	private String description;
	private Integer location;
	private Integer hp;

	public UserDB() {
		// this.id = id;
	}

	public UserDB(String name, Integer lvl, Integer money, Integer exp, Integer attack, Integer defense,
			String description, Integer location) {
		this.name = name;
		this.lvl = lvl;
		this.money = money;
		this.exp = exp;
		this.attack = attack;
		this.defense = defense;
		this.description = description;
		this.location = location;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Integer getLvl() {
		return lvl;
	}

	public void setLvl(Integer lvl) {
		this.lvl = lvl;
	}

	public Integer getMoney() {
		return money;
	}

	public void setMoney(Integer money) {
		this.money = money;
	}

	public Integer getExp() {
		return exp;
	}

	public void setExp(Integer exp) {
		this.exp = exp;
	}

	public Integer getAttack() {
		return attack;
	}

	public void setAttack(Integer attack) {
		this.attack = attack;
	}

	public Integer getDefense() {
		return defense;
	}

	public void setDefense(Integer defense) {
		this.defense = defense;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public Integer getLocation() {
		return location;
	}

	public void setLocation(Integer location) {
		this.location = location;
	}

	public Integer getHp() {
		return hp;
	}

	public void setHp(Integer hp) {
		this.hp = hp;
	}

	/*
	 * @Override public String toString() { return "User{" + ", name='" + name +
	 * '\'' + ", lvl=" + lvl + '}'; }
	 */
}