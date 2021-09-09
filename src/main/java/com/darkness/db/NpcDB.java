package com.darkness.db;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

//for NPC generation

@Getter
@Setter
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

}