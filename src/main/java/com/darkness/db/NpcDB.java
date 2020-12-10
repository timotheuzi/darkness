package com.darkness.db;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

//for NPC generation

@Entity
@Table(name = "npc")
public class NpcDB {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private int id;

	private String name;
	private String description;
	private Integer attack;
	private Integer defense;
	private Integer location;
	private Integer hp;

	public NpcDB() {
		// this.id = id;
	}

	public NpcDB(String name, String description, Integer attack, Integer defense, Integer location) {
		this.name = name;
		this.description = description;
		this.attack = attack;
		this.defense = defense;
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

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
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

	@Override
	public String toString() {
		return "User{" + ", name='" + name + '\'' + ", description=" + description + '}';
	}
}