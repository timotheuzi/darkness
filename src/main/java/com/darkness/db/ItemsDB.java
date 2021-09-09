package com.darkness.db;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

//item table

@Getter
@Setter
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

}