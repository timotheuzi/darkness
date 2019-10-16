package com.darkness.db;

import javax.persistence.*;

//item table

@Entity
@Table(name = "items")
public class ItemsDB {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private int id;

	private String name;
	private String description;
	private Integer attack;
	private Integer defense;

	public ItemsDB() {
		// this.id = id;
	}

	public ItemsDB(String name, String description, Integer attack, Integer defense) {
		this.name = name;
		this.description = description;
		this.attack = attack;
		this.defense = defense;
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

	@Override
	public String toString() {
		return "User{" + ", name='" + name + '\'' + ", description=" + description + '}';
	}
}