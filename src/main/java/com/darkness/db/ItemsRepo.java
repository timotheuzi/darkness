package com.darkness.db;

import org.springframework.data.repository.CrudRepository;

public interface ItemsRepo extends CrudRepository<ItemsDB, Integer> {
	ItemsDB findById(String id);

	//todo add custom query
	//@Query("SELECT * FROM items where name = :name")
	//Optional selectByName(@Param("name") String name);
}