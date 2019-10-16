package com.darkness.db;

import org.springframework.data.repository.CrudRepository;

public interface ItemsRepo extends CrudRepository<ItemsDB, Integer> {
	ItemsDB findByName(String name);
}