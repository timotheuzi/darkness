package com.darkness;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import com.darkness.utils.Methods;
import com.darkness.db.MapDB;
import com.darkness.db.MapRepo;

import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import static org.mockito.Matchers.anyString;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;
import static org.mockito.Matchers.*;

@RunWith(MockitoJUnitRunner.class)
@SpringBootTest
public class DarknessApplicationTests {
	@Mock
	Methods mockMethods;
	@Mock
	MapDB mockMapDB;
	@Mock
	MapRepo mapRepo;

	@Test
	public void contextLoads() {
	}

	/*
	 * @Test public void CountMaps() { /*methods temp = mock(methods.class); Integer
	 * countMaps = temp.CountMaps();
	 * 
	 * Iterable<mapDB> iterator = mapRepo.findAll(); mapDB list = mock(mapDB.class);
	 * Object object = mock(Object.class);
	 * 
	 * when(iterator.iterator()).toString(); //this is to mock list with one
	 * element, adjust accordingly //when(iterator).hasNext()).thenReturn(true,
	 * false); //when(iterator).next().thenReturn(object);
	 * 
	 * 
	 * //String result = ""; Integer count = 0; //for(mapDB mapDB :
	 * mapRepo.findAll()) //{ // count++; //} System.out.println("our count is:" +
	 * count + " second count " + countMaps); }
	 */

}
